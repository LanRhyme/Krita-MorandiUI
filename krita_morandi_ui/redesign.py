"""
    Plugin for Krita UI Redesign, Copyright (C) 2020 Kapyia, Pedro Reis
    Customized and Enhanced Morandi Theme Engine (C) 2026 LanRhyme
"""

from .qt_compat import *
from krita import *
Application = Krita.instance()
from .nuTools.nttoolbox import ntToolBox
from .nuTools.nttooloptions import ntToolOptions
from . import variables
import xml.etree.ElementTree as ET
from .settings_dialog import MorandiSettingsDialog

class Redesign(Extension):

    usesFlatTheme = False
    usesBorderlessToolbar = False
    usesThinDocumentTabs = False
    usesNuToolbox = False
    usesNuToolOptions = False
    ntTB = None
    ntTO = None
    doc_base_sec = {}
    doc_session_sec = {}
    timer = None
    statusTimeLabel = None

    def __init__(self, parent):
        super().__init__(parent)
        self.doc_base_sec = {}
        self.doc_session_sec = {}

    def setup(self):
        if Application.readSetting("Redesign", "usesFlatTheme", "true") == "true":
            self.usesFlatTheme = True

        if Application.readSetting("Redesign", "usesBorderlessToolbar", "true") == "true":
            self.usesBorderlessToolbar = True

        if Application.readSetting("Redesign", "usesThinDocumentTabs", "true") == "true":
            self.usesThinDocumentTabs = True

        if Application.readSetting("Redesign", "usesNuToolbox", "true") == "true":
            self.usesNuToolbox = True

        if Application.readSetting("Redesign", "usesNuToolOptions", "true") == "true":
            self.usesNuToolOptions = True

        # Load initial color & style settings
        self.loadColorSettings()

        # Initialize editing timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateDocEditTime)
        self.timer.start(1000)

    def updateDocEditTime(self):
        try:
            doc = Application.activeDocument()
            win = Application.activeWindow()
            qwin = win.qwindow() if win else None

            if doc and qwin:
                doc_key = doc.fileName() if doc.fileName() else str(id(doc))
                
                # Fetch base total editing time from Krita's documentInfo XML ONCE per doc
                if doc_key not in self.doc_base_sec:
                    base_sec = 0
                    try:
                        info_xml = doc.documentInfo()
                        if info_xml:
                            root = ET.fromstring(info_xml)
                            for elem in root.iter():
                                if elem.tag.endswith("editing-time"):
                                    base_sec = int(elem.text)
                                    break
                    except Exception:
                        base_sec = 0
                    self.doc_base_sec[doc_key] = base_sec
                    self.doc_session_sec[doc_key] = 0

                # Only increment session time if Krita active window currently has focus
                if qwin.isActiveWindow():
                    self.doc_session_sec[doc_key] += 1

                total_sec = self.doc_base_sec[doc_key] + self.doc_session_sec[doc_key]

                h = total_sec // 3600
                m = (total_sec % 3600) // 60
                s = total_sec % 60
                time_str = f"{h:02d}:{m:02d}:{s:02d}"

                if self.statusTimeLabel:
                    self.statusTimeLabel.setText(f"总编辑时长: {time_str}")
            else:
                if self.statusTimeLabel:
                    self.statusTimeLabel.setText("总编辑时长: --:--:--")
        except (RuntimeError, AttributeError):
            self.statusTimeLabel = None
            if self.timer:
                self.timer.stop()

    def loadColorSettings(self):
        accent_preset = Application.readSetting("Redesign", "accentPreset", "鸢尾紫 (Iris)")
        custom_accent = Application.readSetting("Redesign", "customAccent", "8c829e")
        tone_preset = Application.readSetting("Redesign", "tonePreset", "经典深色莫兰迪 (Dark Morandi)")
        custom_bg = Application.readSetting("Redesign", "customBg", "21201c")
        custom_alt = Application.readSetting("Redesign", "customAlt", "2c2b26")
        radius_preset = Application.readSetting("Redesign", "radiusPreset", "标准经典 (12px)")
        scrollbar_preset = Application.readSetting("Redesign", "scrollbarPreset", "标准 Standard (8px)")
        nu_opacity = int(Application.readSetting("Redesign", "nuOpacity", "90"))

        if accent_preset in variables.ACCENT_PRESETS and variables.ACCENT_PRESETS[accent_preset] != "custom":
            hl = variables.ACCENT_PRESETS[accent_preset]
        else:
            hl = custom_accent

        if tone_preset in variables.TONE_PRESETS and variables.TONE_PRESETS[tone_preset] != ("custom", "custom"):
            bg, alt = variables.TONE_PRESETS[tone_preset]
        else:
            bg, alt = custom_bg, custom_alt

        r = variables.RADIUS_PRESETS.get(radius_preset, 12)
        sb = variables.SCROLLBAR_PRESETS.get(scrollbar_preset, 8)

        title_style = Application.readSetting("Redesign", "dockerTitleStyle", "minimalist")
        focus_hl = Application.readSetting("Redesign", "enableFocusHighlight", "true") == "true"
        custom_qss = Application.readSetting("Redesign", "customQSS", "")

        variables.setColors(hl, bg, alt, radius=r, scrollbar=sb, opacity=nu_opacity,
                            title_style=title_style, focus_hl=focus_hl, user_qss=custom_qss)

    def createActions(self, window):
        qwin = window.qwindow()

        # Add status bar time tracker
        statusBar = qwin.statusBar()
        if statusBar and not self.statusTimeLabel:
            self.statusTimeLabel = QLabel("编辑时长: --:--:--")
            self.statusTimeLabel.setStyleSheet(f"color: #{variables.inactive_text_color}; font-size: 11px; padding: 0 10px; border: none;")
            statusBar.addPermanentWidget(self.statusTimeLabel)

        menu = qwin.menuBar().addMenu("莫兰迪UI")

        action_settings = window.createAction("morandiSettings", "设置与外观微调...", "")
        action_settings.triggered.connect(self.openSettingsDialog)
        menu.addAction(action_settings)

        action_export = window.createAction("morandiExportColors", "导出当前主题方案 (.colors)", "")
        action_export.triggered.connect(self.exportColorsFile)
        menu.addAction(action_export)

        action_json = window.createAction("morandiJsonPreset", "导入/导出配色预设 (JSON)", "")
        action_json.triggered.connect(self.importExportJSONPreset)
        menu.addAction(action_json)

        menu.addSeparator()

        actions = []
        actions.append(window.createAction("toolbarBorder", "无边框工具栏", ""))
        actions[0].setCheckable(True)
        actions[0].setChecked(self.usesBorderlessToolbar)

        actions.append(window.createAction("tabHeight", "细长文档标签", ""))
        actions[1].setCheckable(True)
        actions[1].setChecked(self.usesThinDocumentTabs)

        actions.append(window.createAction("flatTheme", "启用扁平外观", ""))
        actions[2].setCheckable(True)
        actions[2].setChecked(self.usesFlatTheme)

        actions.append(window.createAction("nuToolbox", "悬浮工具箱", ""))
        actions[3].setCheckable(True)
        actions[3].setChecked(self.usesNuToolbox)

        actions.append(window.createAction("nuToolOptions", "悬浮工具选项", ""))
        actions[4].setCheckable(True)

        if Application.readSetting("", "ToolOptionsInDocker", "false") == "true":
            actions[4].setChecked(self.usesNuToolOptions)

        for a in actions:
            menu.addAction(a)

        actions[0].toggled.connect(self.toolbarBorderToggled)
        actions[1].toggled.connect(self.tabHeightToggled)
        actions[2].toggled.connect(self.flatThemeToggled)
        actions[3].toggled.connect(self.nuToolboxToggled)
        actions[4].toggled.connect(self.nuToolOptionsToggled)

        variables.buildFlatTheme()

        if (self.usesNuToolOptions and Application.readSetting("", "ToolOptionsInDocker", "false") == "true"):
            self.ntTO = ntToolOptions(window)

        if self.usesNuToolbox:
            self.ntTB = ntToolBox(window)

        self.rebuildStyleSheet(window.qwindow())

    def openSettingsDialog(self):
        win = Application.activeWindow().qwindow()
        dlg = MorandiSettingsDialog(win, self)
        exec_dialog(dlg)

    def exportColorsFile(self):
        file_path, _ = QFileDialog.getSaveFileName(Application.activeWindow().qwindow(), "导出 Krita 主题文件 (.colors)", "Morandi-Custom.colors", "KDE Color Schemes (*.colors)")
        if file_path:
            variables.saveColorSchemeFile("Morandi-Custom", target_path=file_path)
            msg = QMessageBox()
            msg.setText(f"主题文件已导出至:\n{file_path}")
            exec_dialog(msg)

    def importExportJSONPreset(self):
        self.openSettingsDialog()

    def toolbarBorderToggled(self, toggled):
        Application.writeSetting("Redesign", "usesBorderlessToolbar", str(toggled).lower())
        self.usesBorderlessToolbar = toggled
        self.rebuildStyleSheet(Application.activeWindow().qwindow())

    def flatThemeToggled(self, toggled):
        Application.writeSetting("Redesign", "usesFlatTheme", str(toggled).lower())
        self.usesFlatTheme = toggled
        self.rebuildStyleSheet(Application.activeWindow().qwindow())

    def tabHeightToggled(self, toggled):
        Application.instance().writeSetting("Redesign", "usesThinDocumentTabs", str(toggled).lower())
        self.usesThinDocumentTabs = toggled
        self.rebuildStyleSheet(Application.activeWindow().qwindow())

    def nuToolboxToggled(self, toggled):
        Application.writeSetting("Redesign", "usesNuToolbox", str(toggled).lower())
        self.usesNuToolbox = toggled

        if toggled:
            self.ntTB = ntToolBox(Application.activeWindow())
            self.ntTB.pad.show()
            self.ntTB.updateStyleSheet()
        elif not toggled and self.ntTB:
            self.ntTB.close()
            self.ntTB = None

    def nuToolOptionsToggled(self, toggled):
        if Application.readSetting("", "ToolOptionsInDocker", "false") == "true":
            Application.writeSetting("Redesign", "usesNuToolOptions", str(toggled).lower())
            self.usesNuToolOptions = toggled

            if toggled:
                self.ntTO = ntToolOptions(Application.activeWindow())
                self.ntTO.pad.show()
                self.ntTO.updateStyleSheet()
            elif not toggled and self.ntTO:
                self.ntTO.close()
                self.ntTO = None
        else:
            msg = QMessageBox()
            msg.setText("悬浮工具选项功能需要将工具选项位置设置为'停靠区内'。\n\n" +
                        "您可以在 设置 -> 配置 Krita... -> 常规 -> 工具 -> 工具选项位置 中更改。" +
                        "更改完成后，请重启 Krita。")
            exec_dialog(msg)

    def rebuildStyleSheet(self, window):
        app = QApplication.instance()
        if app:
            palette = app.palette()
            palette.setColor(QPalette.ColorRole.Window, QColor("#" + variables.background))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#" + variables.active_text_color))
            palette.setColor(QPalette.ColorRole.Base, QColor("#" + variables.background))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#" + variables.alternate))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#" + variables.background))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#" + variables.active_text_color))
            palette.setColor(QPalette.ColorRole.Text, QColor("#" + variables.active_text_color))
            palette.setColor(QPalette.ColorRole.Button, QColor("#" + variables.background))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#" + variables.active_text_color))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#" + variables.highlight))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#" + variables.background))
            app.setPalette(palette)

        full_style_sheet = ""

        # Dockers
        if self.usesFlatTheme:
            full_style_sheet += f"\n {variables.scrollbar_css} \n"
            full_style_sheet += f"\n {variables.flat_dock_style} \n"
            full_style_sheet += f"\n {variables.flat_button_style} \n"
            full_style_sheet += f"\n {variables.flat_main_window_style} \n"
            full_style_sheet += f"\n {variables.flat_menu_bar_style} \n"
            full_style_sheet += f"\n {variables.flat_combo_box_style} \n"
            full_style_sheet += f"\n {variables.flat_status_bar_style} \n"
            full_style_sheet += f"\n {variables.flat_tree_view_style} \n"
            if variables.custom_qss_style:
                full_style_sheet += f"\n {variables.custom_qss_style} \n"

        # Toolbar
        if self.usesFlatTheme:
            full_style_sheet += f"\n {variables.flat_toolbar_style} \n"
        elif self.usesBorderlessToolbar:
            full_style_sheet += f"\n {variables.no_borders_style} \n"

        window.setStyleSheet(full_style_sheet)
        if app:
            app.setStyleSheet(full_style_sheet)

        # Overview
        overview = window.findChild(QWidget, 'OverviewDocker')
        overview_style = ""

        if self.usesFlatTheme:
            overview_style += f"\n {variables.flat_overview_docker_style} \n"

        if overview:
            overview.setStyleSheet(overview_style)

        # For document tab
        canvas_style_sheet = ""

        if self.usesFlatTheme:
            canvas_style_sheet += f"\n {variables.flat_tab_base_style} \n"
            if self.usesThinDocumentTabs:
                canvas_style_sheet += f"\n {variables.flat_tab_small_style} \n"
            else:
                canvas_style_sheet += f"\n {variables.flat_tab_big_style} \n"
        else:
            if self.usesThinDocumentTabs:
                canvas_style_sheet += f"\n {variables.small_tab_style} \n"

        canvas = window.centralWidget()
        if canvas:
            canvas.setStyleSheet(canvas_style_sheet)
            canvas.resize(canvas.sizeHint())

        # Update Tool Options stylesheet
        if self.usesNuToolOptions and self.ntTO:
            self.ntTO.updateStyleSheet()

        # Update Toolbox stylesheet
        if self.usesNuToolbox and self.ntTB:
            self.ntTB.updateStyleSheet()

Krita.instance().addExtension(Redesign(Krita.instance()))

"""
    Plugin for Krita UI Redesign, Morandi UI Settings Dialog
    Copyright (C) 2026 LanRhyme
"""

from .qt_compat import *
from krita import Krita
Application = Krita.instance()
from . import variables

class MorandiSettingsDialog(QDialog):
    def __init__(self, parent, redesign_extension):
        super().__init__(parent)
        self.ext = redesign_extension
        self.setWindowTitle("莫兰迪 UI 全功能高级设置 (Morandi UI Settings)")
        self.resize(580, 640)

        # Load settings from Krita Application config
        self.accent_preset = Application.readSetting("Redesign", "accentPreset", "鸢尾紫 (Iris)")
        self.custom_accent = Application.readSetting("Redesign", "customAccent", "8c829e")
        self.tone_preset = Application.readSetting("Redesign", "tonePreset", "经典深色莫兰迪 (Dark Morandi)")
        self.custom_bg = Application.readSetting("Redesign", "customBg", "21201c")
        self.custom_alt = Application.readSetting("Redesign", "customAlt", "2c2b26")

        self.radius_preset = Application.readSetting("Redesign", "radiusPreset", "标准极简 (8px)")
        self.scrollbar_preset = Application.readSetting("Redesign", "scrollbarPreset", "极细 Slim (6px)")
        self.nu_opacity = int(Application.readSetting("Redesign", "nuOpacity", "90"))

        self.docker_title_style = Application.readSetting("Redesign", "dockerTitleStyle", "minimalist")
        self.enable_focus_highlight = Application.readSetting("Redesign", "enableFocusHighlight", "true") == "true"
        self.user_qss = Application.readSetting("Redesign", "customQSS", "")

        self.current_accent = self.resolve_accent()
        self.current_bg, self.current_alt = self.resolve_tone()
        self.current_radius = variables.RADIUS_PRESETS.get(self.radius_preset, 8)
        self.current_scrollbar = variables.SCROLLBAR_PRESETS.get(self.scrollbar_preset, 6)

        self.init_ui()

    def resolve_accent(self):
        if self.accent_preset in variables.ACCENT_PRESETS and variables.ACCENT_PRESETS[self.accent_preset] != "custom":
            return variables.ACCENT_PRESETS[self.accent_preset]
        return self.custom_accent

    def resolve_tone(self):
        if self.tone_preset in variables.TONE_PRESETS and variables.TONE_PRESETS[self.tone_preset] != ("custom", "custom"):
            return variables.TONE_PRESETS[self.tone_preset]
        return self.custom_bg, self.custom_alt

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Tab Widget
        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        # =========================================================================
        # Tab 1: 预设画廊 (Morandi Gallery)
        # =========================================================================
        gallery_tab = QWidget()
        gallery_layout = QVBoxLayout()
        gallery_tab.setLayout(gallery_layout)

        gallery_info = QLabel("点击下方任意莫兰迪全景配色卡，即可一键应用完整的色彩与圆角组合：")
        gallery_info.setWordWrap(True)
        gallery_layout.addWidget(gallery_info)

        gallery_scroll = QScrollArea()
        gallery_scroll.setWidgetResizable(True)
        gallery_scroll_widget = QWidget()
        grid_layout = QGridLayout()
        gallery_scroll_widget.setLayout(grid_layout)

        row, col = 0, 0
        for g_name, g_data in variables.GALLERY_PRESETS.items():
            card = QGroupBox(g_name)
            card_layout = QVBoxLayout()
            card.setLayout(card_layout)

            swatch_layout = QHBoxLayout()
            for c_hex in [g_data["bg"], g_data["alt"], g_data["hl"]]:
                swatch = QLabel()
                swatch.setFixedHeight(24)
                swatch.setStyleSheet(f"background-color: #{c_hex}; border-radius: 4px;")
                swatch_layout.addWidget(swatch)

            btn_apply_g = QPushButton("一键套用")
            btn_apply_g.setStyleSheet("padding: 4px; font-weight: bold;")
            btn_apply_g.clicked.connect(lambda _, d=g_data, name=g_name: self.apply_gallery_preset(name, d))

            card_layout.addLayout(swatch_layout)
            card_layout.addWidget(btn_apply_g)

            grid_layout.addWidget(card, row, col)
            col += 1
            if col > 1:
                col = 0
                row += 1

        gallery_scroll.setWidget(gallery_scroll_widget)
        gallery_layout.addWidget(gallery_scroll)
        tabs.addTab(gallery_tab, "预设画廊")

        # =========================================================================
        # Tab 2: 色彩与调性 (Colors & Tones)
        # =========================================================================
        color_tab = QWidget()
        color_layout = QVBoxLayout()
        color_tab.setLayout(color_layout)

        accent_group = QGroupBox("界面强调色 (Accent Color)")
        accent_form = QFormLayout()
        accent_group.setLayout(accent_form)

        self.accent_combo = QComboBox()
        for name in variables.ACCENT_PRESETS.keys():
            self.accent_combo.addItem(name)
        if self.accent_preset in variables.ACCENT_PRESETS:
            self.accent_combo.setCurrentText(self.accent_preset)

        self.accent_btn = QPushButton("自定义颜色")
        self.accent_btn.setFixedWidth(110)
        self.update_btn_color(self.accent_btn, self.current_accent)
        self.accent_btn.clicked.connect(self.pick_accent_color)

        accent_box = QHBoxLayout()
        accent_box.addWidget(self.accent_combo)
        accent_box.addWidget(self.accent_btn)
        accent_form.addRow("强调色预设:", accent_box)
        color_layout.addWidget(accent_group)

        tone_group = QGroupBox("整体色调 (Overall Tone)")
        tone_form = QFormLayout()
        tone_group.setLayout(tone_form)

        self.tone_combo = QComboBox()
        for name in variables.TONE_PRESETS.keys():
            self.tone_combo.addItem(name)
        if self.tone_preset in variables.TONE_PRESETS:
            self.tone_combo.setCurrentText(self.tone_preset)

        self.bg_btn = QPushButton("背景色")
        self.bg_btn.setFixedWidth(90)
        self.update_btn_color(self.bg_btn, self.current_bg)
        self.bg_btn.clicked.connect(self.pick_bg_color)

        self.alt_btn = QPushButton("次要色")
        self.alt_btn.setFixedWidth(90)
        self.update_btn_color(self.alt_btn, self.current_alt)
        self.alt_btn.clicked.connect(self.pick_alt_color)

        tone_box = QHBoxLayout()
        tone_box.addWidget(self.tone_combo)
        tone_box.addWidget(self.bg_btn)
        tone_box.addWidget(self.alt_btn)
        tone_form.addRow("调性预设:", tone_box)
        color_layout.addWidget(tone_group)

        json_group = QGroupBox("莫兰迪配色预设导入/导出 (JSON)")
        json_layout = QHBoxLayout()
        json_group.setLayout(json_layout)

        self.btn_export_json = QPushButton("导出 JSON 预设")
        self.btn_export_json.clicked.connect(self.export_json_preset)

        self.btn_import_json = QPushButton("导入 JSON 预设")
        self.btn_import_json.clicked.connect(self.import_json_preset)

        json_layout.addWidget(self.btn_export_json)
        json_layout.addWidget(self.btn_import_json)
        color_layout.addWidget(json_group)

        tabs.addTab(color_tab, "色彩与调性")

        # =========================================================================
        # Tab 3: 界面与标题栏 (UI & Dockers)
        # =========================================================================
        style_tab = QWidget()
        style_layout = QVBoxLayout()
        style_tab.setLayout(style_layout)

        ui_group = QGroupBox("部件外观与标题栏 (UI & Dockers)")
        ui_form = QFormLayout()
        ui_group.setLayout(ui_form)

        self.cb_flat = QCheckBox("启用莫兰迪扁平外观")
        self.cb_flat.setChecked(self.ext.usesFlatTheme)

        self.cb_borderless = QCheckBox("无边框工具栏")
        self.cb_borderless.setChecked(self.ext.usesBorderlessToolbar)

        self.cb_thin_tabs = QCheckBox("细长文档标签页")
        self.cb_thin_tabs.setChecked(self.ext.usesThinDocumentTabs)

        self.cb_focus_hl = QCheckBox("高亮活动/鼠标悬停面板边框")
        self.cb_focus_hl.setChecked(self.enable_focus_highlight)

        self.cb_canvas_sync = QCheckBox("画布背景/围栏颜色自动同步 (Canvas Surround Sync)")
        self.cb_canvas_sync.setChecked(getattr(self.ext, 'usesCanvasSync', True))

        self.title_style_combo = QComboBox()
        self.title_style_combo.addItem("标准极简 (Minimalist)", "minimalist")
        self.title_style_combo.addItem("隐藏标题栏 (Hidden Titles)", "hidden")
        self.title_style_combo.addItem("胶囊高亮 (Pill Accent Title)", "pill")
        if self.docker_title_style == "hidden":
            self.title_style_combo.setCurrentIndex(1)
        elif self.docker_title_style == "pill":
            self.title_style_combo.setCurrentIndex(2)
        else:
            self.title_style_combo.setCurrentIndex(0)

        self.radius_combo = QComboBox()
        for r_name in variables.RADIUS_PRESETS.keys():
            self.radius_combo.addItem(r_name)
        if self.radius_preset in variables.RADIUS_PRESETS:
            self.radius_combo.setCurrentText(self.radius_preset)

        self.scrollbar_combo = QComboBox()
        for s_name in variables.SCROLLBAR_PRESETS.keys():
            self.scrollbar_combo.addItem(s_name)
        if self.scrollbar_preset in variables.SCROLLBAR_PRESETS:
            self.scrollbar_combo.setCurrentText(self.scrollbar_preset)

        ui_form.addRow("外观风格:", self.cb_flat)
        ui_form.addRow("工具栏风格:", self.cb_borderless)
        ui_form.addRow("标签页风格:", self.cb_thin_tabs)
        ui_form.addRow("焦点边框:", self.cb_focus_hl)
        ui_form.addRow("画布围栏同步:", self.cb_canvas_sync)
        ui_form.addRow("停靠面板标题:", self.title_style_combo)
        ui_form.addRow("圆角弧度:", self.radius_combo)
        ui_form.addRow("滚动条规格:", self.scrollbar_combo)

        style_layout.addWidget(ui_group)
        tabs.addTab(style_tab, "界面与标题栏")

        # =========================================================================
        # Tab 4: 悬浮部件 (Floating NuTools)
        # =========================================================================
        nu_tab = QWidget()
        nu_layout = QVBoxLayout()
        nu_tab.setLayout(nu_layout)

        nu_group = QGroupBox("悬浮部件控制 (Floating NuTools)")
        nu_form = QFormLayout()
        nu_group.setLayout(nu_form)

        self.cb_nutoolbox = QCheckBox("悬浮工具箱 (Nu Toolbox)")
        self.cb_nutoolbox.setChecked(self.ext.usesNuToolbox)

        self.cb_nutooloptions = QCheckBox("悬浮工具选项 (Nu Tool Options)")
        self.cb_nutooloptions.setChecked(self.ext.usesNuToolOptions)

        self.opacity_slider = QSlider(Orientation_Horizontal)
        self.opacity_slider.setRange(0, 100)
        self.opacity_slider.setValue(self.nu_opacity)

        self.opacity_label = QLabel(f"{self.nu_opacity}%")
        self.opacity_slider.valueChanged.connect(lambda v: self.opacity_label.setText(f"{v}%"))

        op_box = QHBoxLayout()
        op_box.addWidget(self.opacity_slider)
        op_box.addWidget(self.opacity_label)

        nu_form.addRow("悬浮工具箱:", self.cb_nutoolbox)
        nu_form.addRow("悬浮工具选项:", self.cb_nutooloptions)
        nu_form.addRow("悬浮窗不透明度:", op_box)

        nu_layout.addWidget(nu_group)
        tabs.addTab(nu_tab, "悬浮部件")

        # =========================================================================
        # Tab 5: 主题导出 & 自定义 QSS (Theme Export & Custom QSS)
        # =========================================================================
        advanced_tab = QWidget()
        advanced_layout = QVBoxLayout()
        advanced_tab.setLayout(advanced_layout)

        exp_group = QGroupBox("导出与安装 Krita 主题文件 (.colors)")
        exp_form = QFormLayout()
        exp_group.setLayout(exp_form)

        self.theme_name_edit = QLineEdit("Morandi-Custom")
        exp_form.addRow("主题方案名称:", self.theme_name_edit)

        exp_btn_box = QHBoxLayout()
        self.btn_gen_internal = QPushButton("安装到 Krita 主题库")
        self.btn_gen_internal.clicked.connect(self.install_theme_internal)

        self.btn_export_colors_file = QPushButton("导出 .colors 文件...")
        self.btn_export_colors_file.clicked.connect(self.export_colors_to_file)

        self.btn_export_gpl = QPushButton("导出莫兰迪绘画色板 (.gpl)")
        self.btn_export_gpl.clicked.connect(self.export_gpl_palette)

        exp_btn_box.addWidget(self.btn_gen_internal)
        exp_btn_box.addWidget(self.btn_export_colors_file)
        exp_btn_box.addWidget(self.btn_export_gpl)

        exp_group.layout().addRow(exp_btn_box)
        advanced_layout.addWidget(exp_group)

        qss_group = QGroupBox("高级自定义 QSS 样式注入 (Custom QSS Code)")
        qss_box_layout = QVBoxLayout()
        qss_group.setLayout(qss_box_layout)

        self.qss_editor = QPlainTextEdit()
        self.qss_editor.setPlaceholderText("在此处添加自定义 QSS 代码规则，例如:\nQGraphicsView { background-color: #21201c; }")
        self.qss_editor.setPlainText(self.user_qss)

        qss_box_layout.addWidget(self.qss_editor)
        advanced_layout.addWidget(qss_group)

        tabs.addTab(advanced_tab, "高级与 QSS")

        # Signals
        self.accent_combo.currentIndexChanged.connect(self.on_accent_changed)
        self.tone_combo.currentIndexChanged.connect(self.on_tone_changed)
        self.radius_combo.currentIndexChanged.connect(self.on_radius_changed)
        self.scrollbar_combo.currentIndexChanged.connect(self.on_scrollbar_changed)

        # Bottom buttons
        btn_box = QHBoxLayout()
        self.btn_apply = QPushButton("应用")
        self.btn_apply.clicked.connect(self.apply_changes)

        self.btn_save = QPushButton("保存并关闭")
        self.btn_save.clicked.connect(self.save_and_close)

        self.btn_cancel = QPushButton("取消")
        self.btn_cancel.clicked.connect(self.reject)

        btn_box.addStretch()
        btn_box.addWidget(self.btn_apply)
        btn_box.addWidget(self.btn_save)
        btn_box.addWidget(self.btn_cancel)

        main_layout.addLayout(btn_box)

    def apply_gallery_preset(self, g_name, g_data):
        self.current_accent = g_data["hl"]
        self.custom_accent = g_data["hl"]
        self.current_bg = g_data["bg"]
        self.custom_bg = g_data["bg"]
        self.current_alt = g_data["alt"]
        self.custom_alt = g_data["alt"]
        self.current_radius = g_data.get("radius", 8)

        self.update_btn_color(self.accent_btn, self.current_accent)
        self.update_btn_color(self.bg_btn, self.current_bg)
        self.update_btn_color(self.alt_btn, self.current_alt)
        self.accent_combo.setCurrentText("自定义 (Custom)")
        self.tone_combo.setCurrentText("自定义 (Custom)")

        for r_name, r_val in variables.RADIUS_PRESETS.items():
            if r_val == self.current_radius:
                self.radius_combo.setCurrentText(r_name)
                break

        self.apply_changes()

    def update_btn_color(self, btn, hex_color):
        hex_str = hex_color.lstrip("#")
        btn.setStyleSheet(f"background-color: #{hex_str}; color: #ffffff; border-radius: 4px; font-weight: bold;")

    def on_accent_changed(self, idx):
        name = self.accent_combo.currentText()
        self.accent_preset = name
        self.current_accent = self.resolve_accent()
        self.update_btn_color(self.accent_btn, self.current_accent)

    def on_tone_changed(self, idx):
        name = self.tone_combo.currentText()
        self.tone_preset = name
        self.current_bg, self.current_alt = self.resolve_tone()
        self.update_btn_color(self.bg_btn, self.current_bg)
        self.update_btn_color(self.alt_btn, self.current_alt)

    def on_radius_changed(self, idx):
        name = self.radius_combo.currentText()
        self.radius_preset = name
        self.current_radius = variables.RADIUS_PRESETS.get(name, 8)

    def on_scrollbar_changed(self, idx):
        name = self.scrollbar_combo.currentText()
        self.scrollbar_preset = name
        self.current_scrollbar = variables.SCROLLBAR_PRESETS.get(name, 6)

    def pick_accent_color(self):
        col = QColorDialog.getColor(QColor("#" + self.current_accent), self, "选择强调色")
        if col.isValid():
            self.custom_accent = col.name().lstrip("#")
            self.current_accent = self.custom_accent
            self.accent_combo.setCurrentText("自定义 (Custom)")
            self.update_btn_color(self.accent_btn, self.current_accent)

    def pick_bg_color(self):
        col = QColorDialog.getColor(QColor("#" + self.current_bg), self, "选择背景色")
        if col.isValid():
            self.custom_bg = col.name().lstrip("#")
            self.current_bg = self.custom_bg
            self.tone_combo.setCurrentText("自定义 (Custom)")
            self.update_btn_color(self.bg_btn, self.current_bg)

    def pick_alt_color(self):
        col = QColorDialog.getColor(QColor("#" + self.current_alt), self, "选择次要色")
        if col.isValid():
            self.custom_alt = col.name().lstrip("#")
            self.current_alt = self.custom_alt
            self.tone_combo.setCurrentText("自定义 (Custom)")
            self.update_btn_color(self.alt_btn, self.current_alt)

    def export_json_preset(self):
        self.apply_changes()
        file_path, _ = QFileDialog.getSaveFileName(self, "导出配色预设 JSON", "morandi_preset.json", "JSON Files (*.json)")
        if file_path:
            variables.exportPresetJSON(file_path)
            QMessageBox.information(self, "导出成功", f"配色预设已导出至:\n{file_path}")

    def import_json_preset(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "导入配色预设 JSON", "", "JSON Files (*.json)")
        if file_path:
            try:
                variables.importPresetJSON(file_path)
                self.current_accent = variables.highlight
                self.current_bg = variables.background
                self.current_alt = variables.alternate
                self.current_radius = variables.border_radius
                self.current_scrollbar = variables.scrollbar_width
                self.opacity_slider.setValue(variables.nu_opacity)
                self.qss_editor.setPlainText(variables.custom_qss)
                self.update_btn_color(self.accent_btn, self.current_accent)
                self.update_btn_color(self.bg_btn, self.current_bg)
                self.update_btn_color(self.alt_btn, self.current_alt)
                self.accent_combo.setCurrentText("自定义 (Custom)")
                self.tone_combo.setCurrentText("自定义 (Custom)")
                self.apply_changes()
                QMessageBox.information(self, "导入成功", "已成功加载并应用 JSON 配色预设")
            except Exception as e:
                QMessageBox.warning(self, "导入失败", f"无法解析配色预设文件: {e}")

    def install_theme_internal(self):
        self.apply_changes()
        name = self.theme_name_edit.text().strip() or "Morandi-Custom"
        path = variables.saveColorSchemeFile(name)
        QMessageBox.information(self, "主题已安装", f"已生成主题方案并安装至 Krita 配色目录:\n{path}\n\n您可以在 软件设置 -> 主题 中启用该配色方案")

    def export_colors_to_file(self):
        self.apply_changes()
        name = self.theme_name_edit.text().strip() or "Morandi-Custom"
        file_path, _ = QFileDialog.getSaveFileName(self, "导出 Krita 主题文件 (.colors)", f"{name}.colors", "KDE Color Schemes (*.colors)")
        if file_path:
            variables.saveColorSchemeFile(name, target_path=file_path)
            QMessageBox.information(self, "导出成功", f"主题文件已保存至:\n{file_path}")

    def apply_changes(self):
        self.ext.usesFlatTheme = self.cb_flat.isChecked()
        self.ext.usesBorderlessToolbar = self.cb_borderless.isChecked()
        self.ext.usesThinDocumentTabs = self.cb_thin_tabs.isChecked()
        self.ext.usesCanvasSync = self.cb_canvas_sync.isChecked()

        if self.ext.usesNuToolbox != self.cb_nutoolbox.isChecked():
            self.ext.nuToolboxToggled(self.cb_nutoolbox.isChecked())
        if self.ext.usesNuToolOptions != self.cb_nutooloptions.isChecked():
            self.ext.nuToolOptionsToggled(self.cb_nutooloptions.isChecked())

        title_style_val = self.title_style_combo.currentData() or "minimalist"
        focus_hl_val = self.cb_focus_hl.isChecked()
        user_qss_val = self.qss_editor.toPlainText()

        variables.setColors(self.current_accent, self.current_bg, self.current_alt,
                             radius=self.current_radius, scrollbar=self.current_scrollbar,
                             opacity=self.opacity_slider.value(), title_style=title_style_val,
                             focus_hl=focus_hl_val, user_qss=user_qss_val)

        # Save settings to Krita config
        Application.writeSetting("Redesign", "usesCanvasSync", str(self.cb_canvas_sync.isChecked()).lower())
        Application.writeSetting("Redesign", "accentPreset", self.accent_combo.currentText())
        Application.writeSetting("Redesign", "customAccent", self.custom_accent)
        Application.writeSetting("Redesign", "tonePreset", self.tone_combo.currentText())
        Application.writeSetting("Redesign", "customBg", self.custom_bg)
        Application.writeSetting("Redesign", "customAlt", self.custom_alt)
        Application.writeSetting("Redesign", "radiusPreset", self.radius_combo.currentText())
        Application.writeSetting("Redesign", "scrollbarPreset", self.scrollbar_combo.currentText())
        Application.writeSetting("Redesign", "nuOpacity", str(self.opacity_slider.value()))

        Application.writeSetting("Redesign", "dockerTitleStyle", title_style_val)
        Application.writeSetting("Redesign", "enableFocusHighlight", str(focus_hl_val).lower())
        Application.writeSetting("Redesign", "customQSS", user_qss_val)

        Application.writeSetting("Redesign", "usesFlatTheme", str(self.cb_flat.isChecked()).lower())
        Application.writeSetting("Redesign", "usesBorderlessToolbar", str(self.cb_borderless.isChecked()).lower())
        Application.instance().writeSetting("Redesign", "usesThinDocumentTabs", str(self.cb_thin_tabs.isChecked()).lower())

        self.ext.rebuildStyleSheet(Application.activeWindow().qwindow())

    def save_and_close(self):
        self.apply_changes()
        self.accept()

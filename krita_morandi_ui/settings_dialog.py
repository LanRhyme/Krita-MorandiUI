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
        self.setWindowTitle("莫兰迪 UI 设置 (Morandi UI Settings)")
        self.resize(540, 580)

        # Load settings from Krita Application config
        self.accent_preset = Application.readSetting("Redesign", "accentPreset", "鸢尾紫 (Iris)")
        self.custom_accent = Application.readSetting("Redesign", "customAccent", "8c829e")
        self.tone_preset = Application.readSetting("Redesign", "tonePreset", "经典深色莫兰迪 (Dark Morandi)")
        self.custom_bg = Application.readSetting("Redesign", "customBg", "21201c")
        self.custom_alt = Application.readSetting("Redesign", "customAlt", "2c2b26")

        self.radius_preset = Application.readSetting("Redesign", "radiusPreset", "标准经典 (12px)")
        self.scrollbar_preset = Application.readSetting("Redesign", "scrollbarPreset", "标准 Standard (8px)")
        self.nu_opacity = int(Application.readSetting("Redesign", "nuOpacity", "90"))

        self.current_accent = self.resolve_accent()
        self.current_bg, self.current_alt = self.resolve_tone()
        self.current_radius = variables.RADIUS_PRESETS.get(self.radius_preset, 12)
        self.current_scrollbar = variables.SCROLLBAR_PRESETS.get(self.scrollbar_preset, 8)

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

        # Tab 1: Colors & Palettes
        color_tab = QWidget()
        color_layout = QVBoxLayout()
        color_tab.setLayout(color_layout)

        # Accent Group
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

        # Tone Group
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

        # Import / Export JSON Preset Group
        json_group = QGroupBox("莫兰迪配色预设导入/导出 (JSON Presets)")
        json_layout = QHBoxLayout()
        json_group.setLayout(json_layout)

        self.btn_export_json = QPushButton("导出配色预设 (JSON)")
        self.btn_export_json.clicked.connect(self.export_json_preset)

        self.btn_import_json = QPushButton("导入配色预设 (JSON)")
        self.btn_import_json.clicked.connect(self.import_json_preset)

        json_layout.addWidget(self.btn_export_json)
        json_layout.addWidget(self.btn_import_json)
        color_layout.addWidget(json_group)

        tabs.addTab(color_tab, "配色方案")

        # Tab 2: UI Style & Layout
        style_tab = QWidget()
        style_layout = QVBoxLayout()
        style_tab.setLayout(style_layout)

        ui_group = QGroupBox("部件与细节外观 (UI Styling)")
        ui_form = QFormLayout()
        ui_group.setLayout(ui_form)

        self.cb_flat = QCheckBox("启用莫兰迪扁平外观")
        self.cb_flat.setChecked(self.ext.usesFlatTheme)

        self.cb_borderless = QCheckBox("无边框工具栏")
        self.cb_borderless.setChecked(self.ext.usesBorderlessToolbar)

        self.cb_thin_tabs = QCheckBox("细长文档标签页")
        self.cb_thin_tabs.setChecked(self.ext.usesThinDocumentTabs)

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
        ui_form.addRow("圆角弧度:", self.radius_combo)
        ui_form.addRow("滚动条规格:", self.scrollbar_combo)

        style_layout.addWidget(ui_group)
        tabs.addTab(style_tab, "界面细致微调")

        # Tab 3: NuTools Floating Dockers
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

        # Tab 4: Theme File Exporter (.colors)
        exporter_tab = QWidget()
        exporter_layout = QVBoxLayout()
        exporter_tab.setLayout(exporter_layout)

        exp_group = QGroupBox("导出与安装 Krita 配色方案 (.colors)")
        exp_form = QFormLayout()
        exp_group.setLayout(exp_form)

        self.theme_name_edit = QLineEdit("Morandi-Custom")
        exp_form.addRow("主题方案名称:", self.theme_name_edit)

        exp_btn_box = QVBoxLayout()
        self.btn_gen_internal = QPushButton("安装到 Krita 主题库 (软件设置 -> 主题中可拔选)")
        self.btn_gen_internal.clicked.connect(self.install_theme_internal)

        self.btn_export_colors_file = QPushButton("导出 .colors 文件到任意路径...")
        self.btn_export_colors_file.clicked.connect(self.export_colors_to_file)

        exp_btn_box.addWidget(self.btn_gen_internal)
        exp_btn_box.addWidget(self.btn_export_colors_file)

        exp_group.layout().addRow(exp_btn_box)
        exporter_layout.addWidget(exp_group)
        tabs.addTab(exporter_tab, "主题文件导出")

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
        self.current_radius = variables.RADIUS_PRESETS.get(name, 12)

    def on_scrollbar_changed(self, idx):
        name = self.scrollbar_combo.currentText()
        self.scrollbar_preset = name
        self.current_scrollbar = variables.SCROLLBAR_PRESETS.get(name, 8)

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

        if self.ext.usesNuToolbox != self.cb_nutoolbox.isChecked():
            self.ext.nuToolboxToggled(self.cb_nutoolbox.isChecked())
        if self.ext.usesNuToolOptions != self.cb_nutooloptions.isChecked():
            self.ext.nuToolOptionsToggled(self.cb_nutooloptions.isChecked())

        variables.setColors(self.current_accent, self.current_bg, self.current_alt,
                            radius=self.current_radius, scrollbar=self.current_scrollbar,
                            opacity=self.opacity_slider.value())

        # Save settings to Krita config
        Application.writeSetting("Redesign", "accentPreset", self.accent_combo.currentText())
        Application.writeSetting("Redesign", "customAccent", self.custom_accent)
        Application.writeSetting("Redesign", "tonePreset", self.tone_combo.currentText())
        Application.writeSetting("Redesign", "customBg", self.custom_bg)
        Application.writeSetting("Redesign", "customAlt", self.custom_alt)
        Application.writeSetting("Redesign", "radiusPreset", self.radius_combo.currentText())
        Application.writeSetting("Redesign", "scrollbarPreset", self.scrollbar_combo.currentText())
        Application.writeSetting("Redesign", "nuOpacity", str(self.opacity_slider.value()))

        Application.writeSetting("Redesign", "usesFlatTheme", str(self.cb_flat.isChecked()).lower())
        Application.writeSetting("Redesign", "usesBorderlessToolbar", str(self.cb_borderless.isChecked()).lower())
        Application.instance().writeSetting("Redesign", "usesThinDocumentTabs", str(self.cb_thin_tabs.isChecked()).lower())

        self.ext.rebuildStyleSheet(Application.activeWindow().qwindow())

    def save_and_close(self):
        self.apply_changes()
        self.accept()

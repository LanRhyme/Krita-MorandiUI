"""
    Plugin for Krita UI Redesign, Copyright (C) 2020 Kapyia, Pedro Reis
    Enhanced Ultra-Flat Morandi Theme Engine (C) 2026 LanRhyme
"""

from .qt_compat import *
from krita import *
import json
from pathlib import Path

# Core color variables
highlight = "8c829e"
background = "21201c"
alternate = "2c2b26"
inactive_text_color = "9f9f9f"
active_text_color = "f3f3f2"

# UI Tweak variables
border_radius = 8
scrollbar_width = 6
font_size = 0  # 0 means default
nu_opacity = 90  # 50 - 100%

small_tab_size = 14

ACCENT_PRESETS = {
    "鸢尾紫 (Iris)": "8c829e",
    "莫兰迪金 (Gold)": "bfa980",
    "玫瑰灰 (Rose)": "c48c90",
    "松绿灰 (Pine)": "7b9c90",
    "海泡绿 (Foam)": "809c95",
    "蜜桃灰 (Peach)": "c79685",
    "天蓝灰 (Sky)": "7f9bb0",
    "芥末黄 (Mustard)": "bda572",
    "瓦松红 (Terracotta)": "be7a6b",
    "薄荷绿 (Mint)": "78a391",
    "鼠尾草青 (Sage)": "8fa382",
    "自定义 (Custom)": "custom",
}

TONE_PRESETS = {
    "经典深色莫兰迪 (Dark Morandi)": ("21201c", "2c2b26"),
    "暖炭灰 (Warm Charcoal)": ("262420", "312f29"),
    "石墨深灰 (Graphite Dark)": ("1d1f21", "282a2d"),
    "冷板岩灰 (Slate Gray)": ("202225", "2b2e33"),
    "极夜黑 (Midnight)": ("161618", "202024"),
    "暖燕麦浅色 (Warm Oatmeal Light)": ("e6e3dd", "dcd8d0"),
    "莫兰迪柔灰 (Soft Gray Light)": ("e3e4e6", "d7d9dc"),
    "自定义 (Custom)": ("custom", "custom"),
}

RADIUS_PRESETS = {
    "极简直角 (0px)": 0,
    "紧凑小圆角 (4px)": 4,
    "标准极简 (8px)": 8,
    "柔和大圆角 (14px)": 14,
}

SCROLLBAR_PRESETS = {
    "极细 Slim (6px)": 6,
    "标准 Standard (8px)": 8,
    "粗体 Large (12px)": 12,
    "隐藏 Hidden (0px)": 0,
}

GALLERY_PRESETS = {
    "北欧苔原 (Nordic Sage)": {"hl": "8fa382", "bg": "212320", "alt": "2b2d2a", "act": "f3f3f2", "inact": "9f9f9f", "radius": 8},
    "京都晚秋 (Kyoto Autumn)": {"hl": "be7a6b", "bg": "241e1c", "alt": "302724", "act": "f5f2f0", "inact": "a09590", "radius": 8},
    "暖粘土 (Warm Clay)": {"hl": "c79685", "bg": "262220", "alt": "312c29", "act": "f5f3f0", "inact": "a39b95", "radius": 10},
    "沙漠玫瑰 (Desert Rose)": {"hl": "c48c90", "bg": "242021", "alt": "2f2a2b", "act": "f4f2f3", "inact": "9f9798", "radius": 8},
    "石墨夜影 (Cyber Graphite)": {"hl": "8c829e", "bg": "1d1f21", "alt": "282a2d", "act": "f0f2f5", "inact": "90959c", "radius": 6},
    "薄荷幽谷 (Soft Mint)": {"hl": "78a391", "bg": "1e2321", "alt": "282e2c", "act": "f1f4f2", "inact": "929c97", "radius": 8},
    "燕麦摩卡 (Mocha Cream)": {"hl": "bfa980", "bg": "25221e", "alt": "302c27", "act": "f6f4f0", "inact": "a29d95", "radius": 8},
    "雾蓝板岩 (Slate Fog)": {"hl": "7f9bb0", "bg": "202225", "alt": "2b2e33", "act": "f0f3f6", "inact": "939aa3", "radius": 8},
    "侘寂暮色 (Wabi-Sabi Dusk)": {"hl": "bda572", "bg": "21201d", "alt": "2c2a26", "act": "f4f3ef", "inact": "9e9a90", "radius": 8},
    "极夜紫灰 (Midnight Plum)": {"hl": "8c829e", "bg": "161618", "alt": "202024", "act": "f3f3f5", "inact": "9898a0", "radius": 4},
    "莫兰迪暖白 (Warm Light)": {"hl": "7b9c90", "bg": "e6e3dd", "alt": "dcd8d0", "act": "282623", "inact": "787570", "radius": 8},
    "冷调柔灰 (Cool Light)": {"hl": "7f9bb0", "bg": "e3e4e6", "alt": "d7d9dc", "act": "202225", "inact": "70737a", "radius": 8},
}

docker_title_style = "minimalist"  # minimalist, hidden, pill
enable_focus_highlight = True
custom_qss = ""

no_borders_style = " QToolBar { border: none; background: transparent; } "

scrollbar_css = ""
flat_tab_base_style = ""
flat_tab_big_style = ""
flat_tab_small_style = ""
flat_main_window_style = ""
flat_button_style = ""
flat_tool_button_style = ""
flat_push_button_style = ""
flat_dock_style = ""
flat_toolbar_style = ""
flat_menu_bar_style = ""
flat_combo_box_style = ""
flat_toolbox_style = ""
flat_status_bar_style = ""
flat_tree_view_style = ""
flat_overview_docker_style = ""
nu_toolbox_style = ""
nu_toggle_button_style = ""
nu_tool_options_style = ""
small_tab_style = ""
custom_qss_style = ""
def ensureSpinboxIcons(fg_hex, bg_hex):
    res_dir = Path.home() / ".local/share/krita/pykrita/krita_morandi_ui/resources"
    res_dir.mkdir(parents=True, exist_ok=True)

    up_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="10" height="8" viewBox="0 0 10 8">
  <polygon points="5,1 9,7 1,7" fill="#{fg_hex}"/>
</svg>'''

    down_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="10" height="8" viewBox="0 0 10 8">
  <polygon points="5,7 9,1 1,1" fill="#{fg_hex}"/>
</svg>'''

    up_hover_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="10" height="8" viewBox="0 0 10 8">
  <polygon points="5,1 9,7 1,7" fill="#{bg_hex}"/>
</svg>'''

    down_hover_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="10" height="8" viewBox="0 0 10 8">
  <polygon points="5,7 9,1 1,1" fill="#{bg_hex}"/>
</svg>'''

    p_up = res_dir / "spinbox_up.svg"
    p_down = res_dir / "spinbox_down.svg"
    p_up_h = res_dir / "spinbox_up_hover.svg"
    p_down_h = res_dir / "spinbox_down_hover.svg"

    p_up.write_text(up_svg, encoding="utf-8")
    p_down.write_text(down_svg, encoding="utf-8")
    p_up_h.write_text(up_hover_svg, encoding="utf-8")
    p_down_h.write_text(down_hover_svg, encoding="utf-8")

    return str(p_up), str(p_down), str(p_up_h), str(p_down_h)

def setColors(hl_color, bg_color, alt_color, act_text="f3f3f2", inact_text="9f9f9f", 
              radius=8, scrollbar=6, opacity=90, title_style="minimalist", focus_hl=True, user_qss=""):
    global highlight, background, alternate, active_text_color, inactive_text_color, border_radius, scrollbar_width, nu_opacity
    global docker_title_style, enable_focus_highlight, custom_qss
    highlight = hl_color.lstrip("#")
    background = bg_color.lstrip("#")
    alternate = alt_color.lstrip("#")
    active_text_color = act_text.lstrip("#")
    inactive_text_color = inact_text.lstrip("#")
    border_radius = int(radius)
    scrollbar_width = int(scrollbar)
    nu_opacity = int(opacity)
    docker_title_style = str(title_style)
    enable_focus_highlight = bool(focus_hl)
    custom_qss = str(user_qss)
    buildFlatTheme()

def buildFlatTheme():
    global scrollbar_css, flat_tab_base_style, flat_tab_big_style, flat_tab_small_style
    global flat_main_window_style, flat_button_style, flat_dock_style
    global flat_toolbar_style, flat_menu_bar_style, flat_combo_box_style
    global flat_toolbox_style, flat_status_bar_style, flat_tree_view_style
    global flat_overview_docker_style, nu_toolbox_style, nu_toggle_button_style
    global nu_tool_options_style, small_tab_style, custom_qss_style

    r = border_radius
    sb_w = scrollbar_width
    r_sm = max(2, r // 2)
    r_lg = r + 4

    p_up, p_down, p_up_h, p_down_h = ensureSpinboxIcons(active_text_color, background)

    small_tab_style = "QTabBar::tab { height: " + str(small_tab_size) + "px; }"

    scrollbar_css = ""
    if sb_w > 0:
        scrollbar_css = f"""
        QScrollBar:vertical {{ 
            width: {sb_w}px; 
            background: transparent;
            margin: 0px;
            border: none !important;
            border-left: none !important;
            border-right: none !important;
        }}
        QScrollBar::handle:vertical {{
            background: #{alternate};
            min-height: 20px;
            border-radius: {max(2, sb_w // 2)}px;
            border: none !important;
        }}
        QScrollBar::handle:vertical:hover {{
            background: #{highlight};
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px;
            width: 0px;
            background: transparent;
            border: none !important;
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: transparent;
            border: none !important;
        }}
        QScrollBar:horizontal {{ 
            height: {sb_w}px; 
            background: transparent;
            margin: 0px;
            border: none !important;
            border-top: none !important;
            border-bottom: none !important;
        }}
        QScrollBar::handle:horizontal {{
            background: #{alternate};
            min-width: 20px;
            border-radius: {max(2, sb_w // 2)}px;
            border: none !important;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: #{highlight};
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
            height: 0px;
            background: transparent;
            border: none !important;
        }}
        QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
            background: transparent;
            border: none !important;
        }}
        QAbstractScrollArea::corner {{
            background: transparent;
            border: none !important;
        }}
        """
    else:
        scrollbar_css = """
        QScrollBar:vertical, QScrollBar:horizontal {
            width: 0px;
            height: 0px;
            background: transparent;
            border: none !important;
        }
        QAbstractScrollArea::corner {
            background: transparent;
            border: none !important;
        }
        """

    flat_overview_docker_style = f"""
        * {{
            background: #{background};
            border: none;
        }} 
        * > QSpinBox {{
            border: none;
            background-color: #{alternate};
            border-radius: {r}px;
            padding: 4px;
        }}
        KisZoomWidget QSlider::groove:horizontal {{
            height: 4px;
            border-radius: 2px;
            background: #{alternate};
        }}
        KisZoomWidget QSlider::handle:horizontal {{
            width: 14px;
            height: 14px;
            margin: -5px 0;
            border-radius: 7px;
            background: #{highlight};
            border: none;
        }}
    """

    flat_tab_base_style = scrollbar_css + f"""
        QTabBar {{
            background-color: #{alternate};
            border: none;
            qproperty-drawBase: 0;
            qproperty-expanding: 1;
        }}
        QTabBar::tab:!selected {{
            background: #{alternate};
            border: none;
            margin: 2px 1px 0px 1px;
            color: #{inactive_text_color};
            padding: 4px 12px;
        }}
        QTabBar::tab:selected {{
            background: #{background};
            border-bottom: 2px solid #{highlight};
            border-top: none;
            margin: 2px 1px 0px 1px;
            color: #{active_text_color};
            padding: 4px 12px;
        }}
        QTabBar::tab:hover {{
           color: #{active_text_color};
           background: #{background};
        }}
    """

    flat_tab_big_style = f"""QTabBar::tab {{
            border-top-right-radius: {r}px;
            border-top-left-radius: {r}px;
        }}"""

    flat_tab_small_style = f""" 
        QTabBar::tab {{
            border: 0px;
            border-top-right-radius: {r}px;
            border-top-left-radius: {r}px;
            height: {small_tab_size}px;
        }}"""

    quick_settings_docker_qss = """
        QuickSettingsDocker QListView {
            qproperty-iconSize: 32px 32px;
            qproperty-gridSize: 36px 48px;
            font-size: 10px;
        }
        QuickSettingsDocker QListView::item {
            margin: 0px;
            padding: 0px;
        }
    """

    flat_main_window_style = f"""
        QMainWindow, QMainWindow::separator {{
            background-color: #{background};
            border: none !important;
        }}
        QSplitter::handle {{
            background-color: #{background};
            border: none !important;
        }}
        QSplitter::handle:horizontal {{
            width: 0px !important;
            background: transparent !important;
        }}
        QSplitter::handle:vertical {{
            height: 0px !important;
            background: transparent !important;
        }}
        QFrame, QAbstractScrollArea, #qt_scrollarea_viewport {{
            border: none !important;
            outline: none !important;
        }}
        QHeaderView {{
            background: #{alternate};
            border: none !important;
        }}
        QHeaderView::section {{
            background: #{alternate};
            color: #{active_text_color};
            border: none !important;
            border-right: none !important;
            border-bottom: none !important;
            padding: 4px;
        }}
        QLineEdit, QSpinBox, QDoubleSpinBox, KisDoubleSliderSpinBox, QAbstractSpinBox {{
            background: #{alternate};
            color: #{active_text_color};
            border: none !important;
            border-radius: {r}px;
            padding: 1px 16px 1px 6px;
            selection-background-color: #{highlight};
            selection-color: #{background};
        }}
        QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, KisDoubleSliderSpinBox:focus, QAbstractSpinBox:focus {{
            border: 1px solid #{highlight} !important;
        }}
        QSpinBox::up-button, QDoubleSpinBox::up-button, QAbstractSpinBox::up-button {{
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 14px;
            border: none !important;
            background: transparent;
            margin: 0px;
            border-top-right-radius: {r}px;
        }}
        QSpinBox::down-button, QDoubleSpinBox::down-button, QAbstractSpinBox::down-button {{
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 14px;
            border: none !important;
            background: transparent;
            margin: 0px;
            border-bottom-right-radius: {r}px;
        }}
        QSpinBox::up-button:hover, QDoubleSpinBox::up-button:hover, QAbstractSpinBox::up-button:hover,
        QSpinBox::down-button:hover, QDoubleSpinBox::down-button:hover, QAbstractSpinBox::down-button:hover {{
            background-color: #{highlight};
        }}
        QSpinBox::up-arrow, QDoubleSpinBox::up-arrow, QAbstractSpinBox::up-arrow {{
            image: url('{p_up}');
            width: 7px;
            height: 5px;
        }}
        QSpinBox::down-arrow, QDoubleSpinBox::down-arrow, QAbstractSpinBox::down-arrow {{
            image: url('{p_down}');
            width: 7px;
            height: 5px;
        }}
        QSpinBox::up-button:hover QSpinBox::up-arrow, QDoubleSpinBox::up-button:hover QDoubleSpinBox::up-arrow {{
            image: url('{p_up_h}');
        }}
        QSpinBox::down-button:hover QSpinBox::down-arrow, QDoubleSpinBox::down-button:hover QDoubleSpinBox::down-arrow {{
            image: url('{p_down_h}');
        }}
        QTabWidget::pane {{
            border: none;
            background: #{background};
            border-radius: {r_lg}px;
        }}
        QSlider::groove:horizontal {{
            background: #{alternate};
            height: 4px;
            border-radius: 2px;
            border: none;
        }}
        QSlider::handle:horizontal {{
            background: #{highlight};
            width: 14px;
            height: 14px;
            margin: -5px 0;
            border-radius: 7px;
            border: none;
        }}
        QSlider::handle:horizontal:hover {{
            background: #{active_text_color};
        }}
        QSlider::sub-page:horizontal {{
            background: #{highlight};
            border-radius: 2px;
        }}
        QSlider::add-page:horizontal {{
            background: #{alternate};
            border-radius: 2px;
        }}
        KisDoubleSliderSpinBox {{
            background: #{alternate};
            border: none;
            border-radius: {r}px;
        }} 
        QCheckBox, QRadioButton {{
            color: #{active_text_color};
            spacing: 6px;
        }}
        QCheckBox::indicator, QRadioButton::indicator {{
            width: 14px;
            height: 14px;
            border-radius: {r_sm}px;
            background-color: #{background};
            border: 1px solid #{alternate};
        }}
        QRadioButton::indicator {{
            border-radius: 7px;
        }}
        QCheckBox::indicator:hover, QRadioButton::indicator:hover {{
            border: 1px solid #{highlight};
        }}
        QCheckBox::indicator:checked, QRadioButton::indicator:checked {{
            background-color: #{highlight};
            border: 1px solid #{highlight};
        }}
        QProgressBar {{
            background-color: #{alternate};
            border: none;
            border-radius: 4px;
            text-align: center;
            color: #{background};
        }}
        QProgressBar::chunk {{
            background-color: #{highlight};
            border-radius: 4px;
        }}
        QGroupBox {{
            border: none;
            margin-top: 14px;
            padding-top: 10px;
        }}
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            padding: 0 4px;
            left: 10px;
            color: #{inactive_text_color};
        }}
        KisWelcomePageWidget {{
            background-color: #{background};
        }}
        KisWelcomePageWidget QListView, QQuickWidget#welcomePage {{
            background-color: #{alternate};
            border-radius: {r_lg}px;
            padding: 16px;
            margin: 8px;
            border: none;
        }}
    """ + quick_settings_docker_qss

    flat_button_style = f"""
        QAbstractButton {{
            background: #{background};
            border: none;
            border-radius: {r}px;
        }}
        QAbstractButton:checked {{
            background: #{alternate};
            color: #{active_text_color};
            border: none;
        }}
        QAbstractButton:hover {{
            background: #{alternate};
            color: #{active_text_color};
            border: none;
        }}
        QAbstractButton[popupMode="1"] {{
            padding-right: 13px;
            border: none;
        }}
        QPushButton {{
            background-color: #{alternate};
            color: #{active_text_color};
            border-radius: {r}px;
            border: none;
            padding: 5px 14px;
        }}
        QPushButton:hover {{
            background-color: #{highlight};
            color: #{background};
        }}
        QPushButton:pressed {{
            background-color: #{background};
            color: #{active_text_color};
        }}
        QToolButton {{
            background-color: transparent;
            border: none;
            border-radius: {r_sm}px;
            padding: 3px;
        }}
        QToolButton:hover {{
            background-color: #{alternate};
        }}
        QToolButton:checked, QToolButton:pressed {{
            background-color: #{highlight};
            color: #{background};
        }}
    """

    flat_dock_style = f""" 
        QAbstractScrollArea {{
            background: #{background};
            border: none;
            border-radius: {r}px;
        }}
        QDockWidget {{
            background: #{background};
            border-radius: {r_lg}px;
            border: none;
            margin: 2px;
            titlebar-close-icon: none;
            titlebar-normal-icon: none;
        }}
        QDockWidget::close-button, QDockWidget::float-button {{
            border: none;
            border-radius: {r_sm}px;
            background: transparent;
        }}
        QDockWidget::close-button:hover, QDockWidget::float-button:hover {{
            background: #{alternate};
        }}
        QDockWidget > * {{
            background-color: #{background};
            border: none;
            border-bottom-right-radius: {r_lg}px;
            border-bottom-left-radius: {r_lg}px;
        }}
        QDockWidget::title {{
            background-color: #{background};
            border: none;
            border-top-left-radius: {r_lg}px;
            border-top-right-radius: {r_lg}px;
            padding: 6px 10px;
            font-weight: bold;
            color: #{inactive_text_color};
        }}
    """

    flat_toolbar_style = f"""
        QToolBar {{
            background-color: #{background};
            border: none;
            border-radius: {r}px;
            margin: 2px;
            padding: 2px;
            spacing: 2px;
        }}
        QToolBar::separator {{
            background-color: #{alternate};
            width: 1px;
            height: 1px;
            margin: 4px;
        }}
        QToolBar > QToolButton {{
            border-radius: {r_sm}px;
            border: none;
            padding: 3px;
            background-color: transparent;
        }}
        QToolBar > QToolButton:hover {{
            background-color: #{alternate};
        }}
        QToolBar > QToolButton:checked, QToolBar > QToolButton:pressed {{
            background-color: #{highlight};
            color: #{background};
        }}
    """

    flat_menu_bar_style = f"""
        QMenuBar {{
            background-color: #{background};
            border: none;
            padding: 2px;
        }}
        QMenuBar::item {{
            background-color: transparent;
            padding: 4px 10px;
            border-radius: {r_sm}px;
            margin: 2px;
            color: #{active_text_color};
        }}
        QMenuBar::item:selected {{
            background-color: #{alternate};
        }}
        QMenu, QToolTip, .KisPopupPalette, QDialog {{
            background-color: #{background};
            border: none;
            border-radius: {r}px;
        }}
        QMenu::item {{
            padding: 6px 16px;
            border-radius: {r_sm}px;
            margin: 2px 4px;
            color: #{active_text_color};
        }}
        QMenu::item:selected {{
            background-color: #{highlight};
            color: #{background};
        }}
        QMenu::separator {{
            height: 1px;
            background-color: #{alternate};
            margin: 4px 8px;
        }}
    """

    flat_combo_box_style = f"""
        QComboBox {{ 
            background-color: #{alternate};
            color: #{active_text_color};
            border: none;
            border-radius: {r}px;
            padding: 4px 12px;
        }}
        QComboBox:hover {{
            background-color: #{highlight};
            color: #{background};
        }}
        QComboBox::drop-down {{
            border: none;
            background: transparent;
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 16px;
        }}
        QComboBox QAbstractItemView {{
            background-color: #{background};
            border: none;
            border-radius: {r}px;
            selection-background-color: #{highlight};
            selection-color: #{background};
            outline: none;
        }}
    """

    flat_toolbox_style = "* > QToolButton { border: none; background: transparent; }"

    flat_status_bar_style = f"""
        QStatusBar {{ 
            background-color: #{background}; 
            max-height: 28px;
            padding: 0px;
            border: none;
        }}
        QStatusBar QLabel, QStatusBar QPushButton, QStatusBar QToolButton {{
            font-size: 11px;
            margin: 0px;
            padding: 0px 4px;
            border: none;
        }}
        QStatusBar KisAngleSelector, QStatusBar KisAngleGauge, QStatusBar QDial {{
            max-width: 0px;
            max-height: 0px;
            margin: 0px;
            padding: 0px;
            border: none;
        }}
    """

    flat_tree_view_style = f"""
    QTreeView, QListView, KisResourceItemListView, KisNodeView, QListWidget, QTableView, 
    #WdgPresetChooser, KisPresetChooser, KisLayerBox {{
        background-color: #{background}; 
        border: none !important;
        padding: 4px;
        border-radius: {r_lg}px;
        outline: none !important;
    }}
    QTreeView::branch {{
        background-color: transparent;
        border: none !important;
    }}
    KisResourceItemListView::item, QListView::item, QListWidget::item, QTableView::item, KisNodeView::item {{
        border-radius: {r}px;
        padding: 4px;
        margin: 1px;
        border: none !important;
        background-color: transparent;
        color: #{active_text_color};
    }}
    KisResourceItemListView::item:selected, QListView::item:selected, QListWidget::item:selected, QTableView::item:selected, KisNodeView::item:selected {{
        background-color: #{highlight} !important;
        color: #{background} !important;
        border: none !important;
    }}
    KisResourceItemListView::item:hover, QListView::item:hover, QListWidget::item:hover, QTableView::item:hover, KisNodeView::item:hover {{
        background-color: #{alternate} !important;
        border: none !important;
    }}
    """

    op_hex = f"{int(255 * nu_opacity / 100):02x}"

    nu_toolbox_style = f"""
            QWidget {{ 
                background-color: #{op_hex}{alternate};
                border-radius: {r_lg}px;
                border: none;
            }}
            .QScrollArea {{ 
                background-color: transparent;
                border: none;
            }}
            QScrollArea * {{ 
                background-color: transparent;
                border: none;
            }}
            QScrollArea QToolTip {{
                background-color: #{active_text_color};
                color: #{background};                         
            }}
            QAbstractButton {{
                background-color: transparent;
                border: none;
                border-radius: {r}px;
            }}
            QAbstractButton:checked {{
                background-color: #{highlight};
                color: #{background};
            }}
            QAbstractButton:hover {{
                background-color: #{op_hex}{background};
            }}
            QAbstractButton:pressed {{
                background-color: #{alternate};
            }}
        """

    nu_toggle_button_style = f"""
        QToolButton {{
            background-color: transparent;
            border: none;
            border-radius: {r}px;
        }}
        QToolButton:hover {{
            background-color: #{highlight};
        }}
        QToolButton:pressed {{
            background-color: #{alternate};
        }}
        """

    nu_tool_options_style = f"""
        #toolOptionsPad {{
            background-color: #{op_hex}{background};
            border-radius: {r_lg}px;
            border: none;
        }}
        #toolOptionsPad > QWidget, #toolOptionsPad QScrollArea, #toolOptionsPad QScrollArea > QWidget {{
            background-color: transparent;
            border-radius: {r_lg}px;
            border: none;
        }}
        """

    custom_qss_style = custom_qss

def generateColorSchemeContent(scheme_name="Morandi-Custom"):
    def rgb_str(hex_c):
        h = hex_c.lstrip("#")
        return f"{int(h[0:2], 16)},{int(h[2:4], 16)},{int(h[4:6], 16)}"

    bg_rgb = rgb_str(background)
    bg_alt_rgb = rgb_str(alternate)
    fg_rgb = rgb_str(active_text_color)
    fg_inact_rgb = rgb_str(inactive_text_color)
    hl_rgb = rgb_str(highlight)

    return f"""[ColorEffects:Disabled]
Color={bg_rgb}
ColorAmount=0
ColorEffect=0
ContrastAmount=0.65
ContrastEffect=1
IntensityAmount=0.1
IntensityEffect=2

[ColorEffects:Inactive]
ChangeSelectionColor=false
Color={fg_inact_rgb}
ColorAmount=0.025
ColorEffect=2
ContrastAmount=0.1
ContrastEffect=2
Enable=false
IntensityAmount=0
IntensityEffect=0

[Colors:Button]
BackgroundAlternate={bg_alt_rgb}
BackgroundNormal={bg_rgb}
DecorationFocus={hl_rgb}
DecorationHover={hl_rgb}
ForegroundActive={hl_rgb}
ForegroundInactive={fg_inact_rgb}
ForegroundLink={hl_rgb}
ForegroundNegative=253,70,99
ForegroundNeutral=189,183,154
ForegroundNormal={fg_rgb}
ForegroundPositive=168,171,160
ForegroundVisited={hl_rgb}

[Colors:Complementary]
BackgroundAlternate={bg_alt_rgb}
BackgroundNormal={bg_rgb}
DecorationFocus={hl_rgb}
DecorationHover={hl_rgb}
ForegroundActive={hl_rgb}
ForegroundInactive={fg_inact_rgb}
ForegroundLink={hl_rgb}
ForegroundNegative=253,70,99
ForegroundNeutral=189,183,154
ForegroundNormal={fg_rgb}
ForegroundPositive=168,171,160
ForegroundVisited={hl_rgb}

[Colors:Header]
BackgroundAlternate={bg_alt_rgb}
BackgroundNormal={bg_rgb}
DecorationFocus={hl_rgb}
DecorationHover={hl_rgb}
ForegroundActive={hl_rgb}
ForegroundInactive={fg_inact_rgb}
ForegroundLink={hl_rgb}
ForegroundNegative=253,70,99
ForegroundNeutral=189,183,154
ForegroundNormal={fg_rgb}
ForegroundPositive=168,171,160
ForegroundVisited={hl_rgb}

[Colors:Selection]
BackgroundAlternate={hl_rgb}
BackgroundNormal={hl_rgb}
DecorationFocus={hl_rgb}
DecorationHover={hl_rgb}
ForegroundActive={bg_rgb}
ForegroundInactive={bg_rgb}
ForegroundLink={bg_rgb}
ForegroundNegative=253,70,99
ForegroundNeutral=189,183,154
ForegroundNormal={bg_rgb}
ForegroundPositive=168,171,160
ForegroundVisited={bg_rgb}

[Colors:Tooltip]
BackgroundAlternate={bg_alt_rgb}
BackgroundNormal={bg_rgb}
DecorationFocus={hl_rgb}
DecorationHover={hl_rgb}
ForegroundActive={hl_rgb}
ForegroundInactive={fg_inact_rgb}
ForegroundLink={hl_rgb}
ForegroundNegative=253,70,99
ForegroundNegative=253,70,99
ForegroundNeutral=189,183,154
ForegroundNormal={fg_rgb}
ForegroundPositive=168,171,160
ForegroundVisited={hl_rgb}

[Colors:View]
BackgroundAlternate={bg_alt_rgb}
BackgroundNormal={bg_rgb}
DecorationFocus={hl_rgb}
DecorationHover={hl_rgb}
ForegroundActive={hl_rgb}
ForegroundInactive={fg_inact_rgb}
ForegroundLink={hl_rgb}
ForegroundNegative=253,70,99
ForegroundNeutral=189,183,154
ForegroundNormal={fg_rgb}
ForegroundPositive=168,171,160
ForegroundVisited={hl_rgb}

[Colors:Window]
BackgroundAlternate={bg_alt_rgb}
BackgroundNormal={bg_rgb}
DecorationFocus={hl_rgb}
DecorationHover={hl_rgb}
ForegroundActive={hl_rgb}
ForegroundInactive={fg_inact_rgb}
ForegroundLink={hl_rgb}
ForegroundNegative=253,70,99
ForegroundNeutral=189,183,154
ForegroundNormal={fg_rgb}
ForegroundPositive=168,171,160
ForegroundVisited={hl_rgb}

[General]
ColorScheme={scheme_name}
Name={scheme_name}
shadeSortColumn=true

[KDE]
contrast=4

[WM]
activeBackground={bg_rgb}
activeBlend={fg_rgb}
activeForeground={fg_rgb}
inactiveBackground={bg_alt_rgb}
inactiveBlend={fg_inact_rgb}
inactiveForeground={fg_inact_rgb}
"""

def saveColorSchemeFile(scheme_name="Morandi-Custom", target_path=None):
    if not target_path:
        target_dir = Path.home() / ".local/share/krita/color-schemes"
        target_dir.mkdir(parents=True, exist_ok=True)
        file_path = target_dir / f"{scheme_name}.colors"
    else:
        file_path = Path(target_path)
    
    content = generateColorSchemeContent(scheme_name)
    file_path.write_text(content, encoding="utf-8")
    return str(file_path)

def exportPresetJSON(target_path):
    data = {
        "highlight": highlight,
        "background": background,
        "alternate": alternate,
        "active_text_color": active_text_color,
        "inactive_text_color": inactive_text_color,
        "border_radius": border_radius,
        "scrollbar_width": scrollbar_width,
        "nu_opacity": nu_opacity
    }
    Path(target_path).write_text(json.dumps(data, indent=2), encoding="utf-8")

def importPresetJSON(source_path):
    content = Path(source_path).read_text(encoding="utf-8")
    data = json.loads(content)
    hl = data.get("highlight", "8c829e")
    bg = data.get("background", "21201c")
    alt = data.get("alternate", "2c2b26")
    act = data.get("active_text_color", "f3f3f2")
    inact = data.get("inactive_text_color", "9f9f9f")
    rad = data.get("border_radius", 8)
    sb = data.get("scrollbar_width", 6)
    op = data.get("nu_opacity", 90)
    setColors(hl, bg, alt, act, inact, rad, sb, op)

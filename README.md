# Krita Morandi UI

<p align="center">
  <a href="https://qm.qq.com/q/mtg1yNCi1q"><img alt="QQ" src="https://img.shields.io/badge/QQ-729283213-12B7F5?style=for-the-badge&logo=qq&logoColor=white"></a>
  <a href="https://afdian.com/a/LanRhyme" target="_blank" rel="noopener noreferrer"><img src="https://img.shields.io/badge/afdian-@LanRhyme-946ce6?style=for-the-badge&logo=afdian&logoColor=white" alt="afdian"></a>
</p>

A standalone, sleek, flat UI redesign and Morandi theme engine plugin for Krita

![Krita Morandi UI Screenshot](https://raw.githubusercontent.com/LanRhyme/Krita-MorandiUI/main/screenshot.png)

## 功能特性

- **丰富强调色预设**: 内置 11 种莫兰迪语义色调（鸢尾紫、莫兰迪金、玫瑰灰、松绿灰、海泡绿、蜜桃灰、天蓝灰、芥末黄、瓦松红、薄荷绿、鼠尾草青等），并支持自定义任意颜色
- **多调性背景主题**: 内置 7 种莫兰迪明暗主题预设（经典深色莫兰迪、暖炭灰、石墨深灰、冷板岩灰、极夜黑、暖燕麦浅色、莫兰迪柔灰等），支持独立配置背景色与次要对比色
- **内置图层标记莫兰迪配色**: 全面替换 Krita 默认的高饱和图层颜色标记（雾蓝、鼠尾草绿、燕麦黄、陶土橘、暖褐、干玫瑰红、极夜紫灰、暖灰）
- **画布围栏背景同步**: 支持画布围栏与背景颜色随莫兰迪主题动态联动
- **平滑微动画**: 悬浮工具箱与属性面板展收淡入淡出、下拉列表与菜单弹出淡入（220ms）、Dockers 面板显示淡入（180ms）
- **界面细节与部件控制**:
  - 圆角弧度调节（直角 0px / 紧凑小圆角 4px / 标准极简 8px / 柔和大圆角 14px）
  - 滚动条规格调节（极细 Slim 6px / 标准 Standard 8px / 粗体 Large 12px / 隐藏 Hidden 0px）
  - 悬浮窗不透明度调节（0% - 100% 动态调节）
  - 极致扁平边框微调（自动消除面板分割线与视口边框）
- **独立主题文件导出 (.colors)**: 一键生成与导出符合 KDE 标准的 Krita 配色方案文件
- **配色预设导入与导出 (JSON)**: 允许用户将莫兰迪配色预设导出为 JSON 文件或导入配置文件
- **跨平台与即时渲染**: 纯 Python + Qt 编写，支持 Windows、Linux 与 macOS；无需重启软件即可实现 QSS 样式与 Qt Palette 实时刷新重绘

## 兼容性说明

本插件兼容 Krita 5.0 及以上版本（同时支持 PyQt5 与 PyQt6 运行环境）

## 目录结构

- `krita_morandi_ui`: 插件核心目录（包含 `redesign.py`, `variables.py`, `settings_dialog.py`, `qt_compat.py` 等）
- `nuTools/`: 悬浮工具箱与悬浮工具选项模块

## 鸣谢与版权声明 (Credits & Copyright)

Based on the original Krita UI Redesign plugin
Original Authors: Kapyia, Pedro Reis (Copyright (C) 2020)
GNU General Public License version 3

# Krita Morandi UI

A standalone, sleek, flat UI redesign and Morandi theme engine plugin for Krita

## 功能特性

- **丰富强调色预设**: 内置 11 种莫兰迪语义色调（鸢尾紫、莫兰迪金、玫瑰灰、松绿灰、海泡绿、蜜桃灰、天蓝灰、芥末黄、瓦松红、薄荷绿、鼠尾草青等），并支持通过原生 `QColorDialog` 调色板自定义任意颜色
- **多调性背景主题**: 内置 7 种莫兰迪明暗主题预设（经典深色莫兰迪、暖炭灰、石墨深灰、冷板岩灰、极夜黑、暖燕麦浅色、莫兰迪柔灰等），支持独立配置背景色与次要对比色
- **部件细节微调**:
  - 圆角弧度调节（直角 0px / 紧凑小圆角 6px / 标准 12px / 柔和大圆角 18px）
  - 滚动条规格调节（极细 Slim 6px / 标准 Standard 8px / 粗体 Large 12px / 隐藏 Hidden 0px）
  - 悬浮窗不透明度调节（50% - 100% 动态调节）
- **独立主题文件导出 (.colors)**: 一键生成与导出符合 KDE 标准的 Krita 配色方案文件（可直接一键安装至 Krita 主题库或导出至任意磁盘位置）
- **配色预设导入与导出 (JSON)**: 允许用户将自己的莫兰迪配色预设导出为 JSON 文件或导入他人分享的配色配置文件
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

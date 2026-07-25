try:
    from PyQt6.QtCore import Qt, QObject, QEvent, QPoint, QSize
    from PyQt6.QtGui import QPalette, QColor
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, QScrollArea,
                                 QToolButton, QPushButton, QLabel, QComboBox, QColorDialog,
                                 QCheckBox, QSlider, QGroupBox, QSpinBox, QFileDialog, QTabWidget,
                                 QLineEdit, QPlainTextEdit, QSizePolicy, QMdiArea, QDockWidget, QMessageBox, QApplication,
                                 QStyleOption, QStylePainter, QStyle, QDialog)
    
    # Enums PyQt6
    MouseButton_LeftButton = Qt.MouseButton.LeftButton
    ToolButtonIconOnly = Qt.ToolButtonStyle.ToolButtonIconOnly
    FocusPolicy_NoFocus = Qt.FocusPolicy.NoFocus
    WindowType_Tool = Qt.WindowType.Tool
    WindowType_FramelessWindowHint = Qt.WindowType.FramelessWindowHint
    WindowType_WindowStaysOnTopHint = Qt.WindowType.WindowStaysOnTopHint
    AlignmentFlag_AlignRight = Qt.AlignmentFlag.AlignRight
    AlignmentFlag_AlignVCenter = Qt.AlignmentFlag.AlignVCenter
    AlignmentFlag_AlignCenter = Qt.AlignmentFlag.AlignCenter
    Orientation_Horizontal = Qt.Orientation.Horizontal
    Orientation_Vertical = Qt.Orientation.Vertical
    ColorRole_WindowText = QPalette.ColorRole.WindowText
    QStyle_PE_Widget = QStyle.PrimitiveElement.PE_Widget

    if not hasattr(QDialog, 'exec_'):
        QDialog.exec_ = QDialog.exec
    if not hasattr(QMessageBox, 'exec_'):
        QMessageBox.exec_ = QMessageBox.exec

except ImportError:
    from PyQt5.QtCore import Qt, QObject, QEvent, QPoint, QSize
    from PyQt5.QtGui import QPalette, QColor
    from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout, QScrollArea,
                                 QToolButton, QPushButton, QLabel, QComboBox, QColorDialog,
                                 QCheckBox, QSlider, QGroupBox, QSpinBox, QFileDialog, QTabWidget,
                                 QLineEdit, QPlainTextEdit, QSizePolicy, QMdiArea, QDockWidget, QMessageBox, QApplication,
                                 QStyleOption, QStylePainter, QStyle, QDialog)
    
    # Enums PyQt5
    MouseButton_LeftButton = Qt.LeftButton
    ToolButtonIconOnly = Qt.ToolButtonIconOnly
    FocusPolicy_NoFocus = Qt.NoFocus
    WindowType_Tool = Qt.Tool
    WindowType_FramelessWindowHint = Qt.FramelessWindowHint
    WindowType_WindowStaysOnTopHint = Qt.WindowStaysOnTopHint
    AlignmentFlag_AlignRight = Qt.AlignRight
    AlignmentFlag_AlignVCenter = Qt.AlignVCenter
    AlignmentFlag_AlignCenter = Qt.AlignCenter
    Orientation_Horizontal = Qt.Horizontal
    Orientation_Vertical = Qt.Vertical
    ColorRole_WindowText = QPalette.WindowText
    QStyle_PE_Widget = QStyle.PE_Widget

def exec_dialog(dialog_or_msg):
    if hasattr(dialog_or_msg, "exec"):
        return dialog_or_msg.exec()
    elif hasattr(dialog_or_msg, "exec_"):
        return dialog_or_msg.exec_()

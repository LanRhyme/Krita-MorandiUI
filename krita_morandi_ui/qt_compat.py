try:
    from PyQt6.QtCore import Qt, QObject, QEvent, QPoint, QSize
    from PyQt6.QtGui import QPalette
    from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QToolButton, QSizePolicy, 
                                 QMdiArea, QDockWidget, QMessageBox, QApplication, QStyleOption, QStylePainter, QStyle)
    
    # Enums PyQt6
    MouseButton_LeftButton = Qt.MouseButton.LeftButton
    ToolButtonIconOnly = Qt.ToolButtonStyle.ToolButtonIconOnly
    FocusPolicy_NoFocus = Qt.FocusPolicy.NoFocus
    WindowType_Tool = Qt.WindowType.Tool
    WindowType_FramelessWindowHint = Qt.WindowType.FramelessWindowHint
    WindowType_WindowStaysOnTopHint = Qt.WindowType.WindowStaysOnTopHint
    AlignmentFlag_AlignRight = Qt.AlignmentFlag.AlignRight
    AlignmentFlag_AlignVCenter = Qt.AlignmentFlag.AlignVCenter
    Orientation_Horizontal = Qt.Orientation.Horizontal
    Orientation_Vertical = Qt.Orientation.Vertical
    ColorRole_WindowText = QPalette.ColorRole.WindowText
    QStyle_PE_Widget = QStyle.PrimitiveElement.PE_Widget
    
except ImportError:
    from PyQt5.QtCore import Qt, QObject, QEvent, QPoint, QSize
    from PyQt5.QtGui import QPalette
    from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QScrollArea, QToolButton, QSizePolicy, 
                                 QMdiArea, QDockWidget, QMessageBox, QApplication, QStyleOption, QStylePainter, QStyle)
    
    # Enums PyQt5
    MouseButton_LeftButton = Qt.LeftButton
    ToolButtonIconOnly = Qt.ToolButtonIconOnly
    FocusPolicy_NoFocus = Qt.NoFocus
    WindowType_Tool = Qt.Tool
    WindowType_FramelessWindowHint = Qt.FramelessWindowHint
    WindowType_WindowStaysOnTopHint = Qt.WindowStaysOnTopHint
    AlignmentFlag_AlignRight = Qt.AlignRight
    AlignmentFlag_AlignVCenter = Qt.AlignVCenter
    Orientation_Horizontal = Qt.Horizontal
    Orientation_Vertical = Qt.Vertical
    ColorRole_WindowText = QPalette.WindowText
    QStyle_PE_Widget = QStyle.PE_Widget

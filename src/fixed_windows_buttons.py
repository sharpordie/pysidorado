import sys

from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QProgressBar,
    QPushButton,
    QStyle,
    QStyleOptionButton,
    QStylePainter,
    QTableWidget,
    QWidget,
)


class FixedWindowsButton(QPushButton):
    """Custom QPushButton that fixes the weird one-pixel space around on Windows systems."""

    def paintEvent(self, event):
        if self.style().proxy().objectName() != "windowsvista":
            super().paintEvent(event)
            return
        opt = QStyleOptionButton()
        self.initStyleOption(opt)
        opt.rect.adjust(-1, -1, 1, 1)
        qp = QStylePainter(self)
        qp.drawControl(QStyle.CE_PushButton, opt)


class Window(QWidget):
    """The main application Window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Example")
        self.layout = QGridLayout()
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.layout.addWidget(QTableWidget(), 0, 0, 1, 3)
        self.loading_bar = QProgressBar()
        self.loading_bar.setTextVisible(False)
        self.loading_bar.setValue(25)
        self.layout.addWidget(self.loading_bar, 1, 0, 1, 1)
        self.refresh_btn = FixedWindowsButton("Refresh")
        self.layout.addWidget(self.refresh_btn, 1, 1, 1, 1)
        self.execute_btn = FixedWindowsButton("Execute")
        self.layout.addWidget(self.execute_btn, 1, 2, 1, 1)
        self.setLayout(self.layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
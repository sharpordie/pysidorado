import sys

from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QProgressBar,
    QPushButton,
    QStyle,
    QStyleOptionButton,
    QStylePainter,
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


class LongRunningProcess(QThread):
    progress_changed = Signal(int)

    def run(self):
        progress = 0
        while progress <= 100:
            self.progress_changed.emit(progress)
            self.msleep(250)
            progress += 10


class Window(QWidget):
    """The main application Window."""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Example")
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(6, 6, 6, 6)
        self.loading_bar = QProgressBar()
        self.loading_bar.setTextVisible(False)
        self.loading_bar.setFixedHeight(25)
        self.layout.addWidget(self.loading_bar)
        self.quit_btn = FixedWindowsButton("Quit")
        self.quit_btn.setFixedHeight(25)
        self.quit_btn.clicked.connect(self.onQuitBtnClicked)
        self.layout.addWidget(self.quit_btn)
        self.run_btn = FixedWindowsButton("Run")
        self.run_btn.setFixedHeight(25)
        self.run_btn.clicked.connect(self.onRunBtnClicked)
        self.layout.addWidget(self.run_btn)
        self.setLayout(self.layout)

    def onRunBtnClicked(self):
        self.run_btn.setText("Loading...")
        self.run_btn.setEnabled(False)
        self.quit_btn.setEnabled(False)
        self.quit_btn.setHidden(True)
        self.calc = LongRunningProcess()
        self.calc.progress_changed.connect(self.onProgressChanged)
        self.calc.finished.connect(self.onProgressFinished)
        self.calc.start()

    def onQuitBtnClicked(self):
        self.close()

    def onProgressChanged(self, value):
        self.loading_bar.setValue(value)

    def onProgressFinished(self):
        self.quit_btn.setHidden(False)
        self.quit_btn.setEnabled(True)
        self.run_btn.setEnabled(True)
        self.run_btn.setText("Run")
        self.loading_bar.setValue(0)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PyQt6.QtCore import Qt

from camera import Camera
from info import Info

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QMainWindow {
                border-image: url("background.jpeg");
            }
        """)


        self.frame = QWidget()
        self.frame.layout = QVBoxLayout()

        self.frame.layout.addWidget(Display())
        self.frame.layout.addStretch()
        self.frame.setLayout(self.frame.layout)

        self.setCentralWidget(self.frame)

        self.showMaximized()
        
class Display(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: #3035d9;
                border-radius: 20px;
            }
        """)


        self.camera = Camera(1)
        self.info = Info()

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.camera)
        self.layout.addWidget(self.info)

        self.setLayout(self.layout)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout

from camera import Camera

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()


        self.frame = QWidget()
        self.frame.layout = QVBoxLayout()

        self.frame.layout.addWidget(Camera(1))
        self.frame.setLayout(self.frame.layout)

        self.setCentralWidget(self.frame)

if __name__ == "__main__":
    app = QApplication([])

    window = MainWindow()
    window.show()

    app.exec()
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class Info(QWidget):
    def __init__(self):
        super().__init__()

        self.tds = InfoLabel("TDS (water clarity)", "ppm")
        self.ph = InfoLabel("pH", "")
        self.weight = InfoLabel("Weight", "g")

        self.layout = QVBoxLayout()
        
        self.layout.addWidget(self.tds)
        self.layout.addWidget(self.ph)
        self.layout.addWidget(self.weight)
        self.layout.addWidget(QLabel("Code available at https://github.com/goldspaghetti/fish"))

        self.setLayout(self.layout)

class InfoLabel(QLabel):
    def __init__(self, name, units):
        super().__init__(f"{name}: 0 {units}")

        self.setStyleSheet("""
            font-weight: 700;
            font-size: 20px;

            color: white;
        """)

        self.name = name
        self.units = units

    def update_value(self, v):
        self.setText(f"{self.name}: {v} {self.units}")
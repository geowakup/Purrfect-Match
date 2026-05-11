from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

class CharacterSelectApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Choose Character")
        self.resize(300, 300)

        layout = QVBoxLayout()

        self.firefly_button = QPushButton("Firefly")
        self.firefly_button.clicked.connect(lambda: self.select_character("firefly"))
        layout.addWidget(self.firefly_button)

        self.cat_button = QPushButton("Cat")
        self.cat_button.clicked.connect(lambda: self.select_character("cat"))
        layout.addWidget(self.cat_button)

        self.dog_button = QPushButton("Dog")
        self.dog_button.clicked.connect(lambda: self.select_character("dog"))
        layout.addWidget(self.dog_button)

        self.setLayout(layout)

        self.parent_window = None

    def select_character(self, name):
        if self.parent_window:
            self.parent_window.change_character(name)

        self.close()
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton

# =========================
# Settings
# =========================
class SettingsApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.resize(300, 300)

        layout = QVBoxLayout()

        self.feed_button = QPushButton("Feed Pet (+20 hunger)")
        self.feed_button.clicked.connect(self.feed_pet)
        layout.addWidget(self.feed_button)

        self.play_button = QPushButton("Play Action")
        self.play_button.clicked.connect(self.play_action)
        layout.addWidget(self.play_button)

        self.setLayout(layout)

        self.pet = None

    def feed_pet(self):
        if self.pet:
            self.pet.hunger = min(100, self.pet.hunger + 20)

    def play_action(self):
        if self.pet:
            self.pet.trigger_random_action()
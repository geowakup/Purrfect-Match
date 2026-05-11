from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QSlider,
    QMessageBox
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut


# =========================
# Settings
# =========================
class SettingsApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.resize(300, 450)

        layout = QVBoxLayout()

        # =========================
        # Advancement Button
        # =========================
        self.advancement_button = QPushButton("Advancements")
        self.advancement_button.clicked.connect(self.show_advancements)
        layout.addWidget(self.advancement_button)

        # =========================
        # Hidden Golden Finger Buttons
        # =========================
        self.feed_button = QPushButton("Feed Pet (+20 hunger)")
        self.feed_button.clicked.connect(self.feed_pet)
        self.feed_button.hide()
        layout.addWidget(self.feed_button)

        self.play_button = QPushButton("Play Action")
        self.play_button.clicked.connect(self.play_action)
        self.play_button.hide()
        layout.addWidget(self.play_button)

        # =========================
        # Master Volume
        # =========================
        self.master_label = QLabel("Master Volume: 100")
        layout.addWidget(self.master_label)

        self.master_slider = QSlider(Qt.Horizontal)
        self.master_slider.setRange(0, 100)
        self.master_slider.setValue(100)
        self.master_slider.valueChanged.connect(self.change_master_volume)
        layout.addWidget(self.master_slider)

        # =========================
        # Background Music Volume
        # =========================
        self.bgm_label = QLabel("Background Music Volume: 100")
        layout.addWidget(self.bgm_label)

        self.bgm_slider = QSlider(Qt.Horizontal)
        self.bgm_slider.setRange(0, 100)
        self.bgm_slider.setValue(100)
        self.bgm_slider.valueChanged.connect(self.change_bgm_volume)
        layout.addWidget(self.bgm_slider)

        self.setLayout(layout)

        self.pet = None

        # =========================
        # Secret Shortcut
        # Ctrl + Shift + G
        # =========================
        self.secret_shortcut = QShortcut(
            QKeySequence("Ctrl+Shift+G"),
            self
        )
        self.secret_shortcut.activated.connect(
            self.toggle_golden_finger
        )

        self.golden_mode = False

    # =========================
    # Advancement Window
    # =========================
    def show_advancements(self):
        advancement_text = (self.parent_window.advancement_manager.get_advancement_text())

        QMessageBox.information(self,"Advancements",advancement_text)

    # =========================
    # Golden Finger Toggle
    # =========================
    def toggle_golden_finger(self):
        self.golden_mode = not self.golden_mode

        self.feed_button.setVisible(self.golden_mode)
        self.play_button.setVisible(self.golden_mode)

        print("Golden Finger:", self.golden_mode)

    # =========================
    # Pet Functions
    # =========================
    def feed_pet(self):
        if self.pet:
            self.pet.hunger = min(100,self.pet.hunger + 20)

        self.parent_window.advancement_manager.add_progress(
            "feed_10"
        )
    def play_action(self):
        if self.pet:
            self.pet.trigger_random_action()

            self.parent_window.advancement_manager.add_progress("play_20")

    # =========================
    # Volume Functions
    # =========================
    def change_master_volume(self, value):
        self.master_label.setText(
            f"Master Volume: {value}"
        )

    def change_bgm_volume(self, value):
        self.bgm_label.setText(
            f"Background Music Volume: {value}"
        )
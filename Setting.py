from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QSlider,
    QMessageBox,
    QInputDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from shop_system import ShopSystem
from styles import load_theme


# =========================
# Settings
# =========================
class SettingsApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.resize(300, 450)

        layout = QVBoxLayout()
        
        #=========================
        # Theme Button
        #=========================
        self.pink_theme_btn = QPushButton("Pink Theme")
        self.dark_theme_btn = QPushButton("Dark Theme")
        self.cyber_theme_btn = QPushButton("Cyber Theme")

        layout.addWidget(self.pink_theme_btn)
        layout.addWidget(self.dark_theme_btn)
        layout.addWidget(self.cyber_theme_btn)

        self.pink_theme_btn.clicked.connect(
        lambda: self.change_theme("pink")
        )

        self.dark_theme_btn.clicked.connect(
        lambda: self.change_theme("dark")
        )

        self.cyber_theme_btn.clicked.connect(
        lambda: self.change_theme("cyber")
        )


        # =========================
        # Advancement Button
        # =========================
        self.advancement_button = QPushButton("Advancements")
        self.advancement_button.clicked.connect(self.show_advancements)
        layout.addWidget(self.advancement_button)

        # =========================
        # Shop Button
        # =========================
        self.shop_button = QPushButton("Open Shop")
        self.shop_button.clicked.connect(self.open_shop)
        layout.addWidget(self.shop_button)

        self.shop_system = ShopSystem()

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
    # Theme Change Function             
    # =========================
    def change_theme(self, theme_name):
        app = QApplication.instance()
        app.setStyleSheet(load_theme(theme_name))
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

    def open_shop(self):
        if self.pet is None:
            QMessageBox.warning(self, "Shop", "Pet data not available.")
            return

        item_lines = []
        for item_name, item_data in self.shop_system.items.items():
            price = item_data.get("price", 0)
            hunger = item_data.get("hunger", 0)
            happiness = item_data.get("happiness", 0)
            item_lines.append(
                f"{item_name}: {price} coins, hunger +{hunger}, happiness +{happiness}"
            )

        item_list = "\n".join(item_lines)
        item_choice, ok = QInputDialog.getText(
            self,
            "Shop",
            f"Available items:\n{item_list}\n\nEnter item name to buy:",
        )

        if not ok or not item_choice:
            return

        item_choice = item_choice.strip().lower()
        success, message = self.shop_system.buy_item(self.pet, item_choice)

        if success:
            QMessageBox.information(self, "Shop", message)
        else:
            QMessageBox.warning(self, "Shop", message)

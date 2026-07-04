from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox
)

from shop_system import ShopSystem


class ShopWindow(QWidget):

    def __init__(self, pet):
        super().__init__()

        self.pet = pet
        self.shop = ShopSystem()

        self.setWindowTitle("Pet Shop")
        self.resize(300, 400)

        self.layout = QVBoxLayout()

        # Coin display
        self.coin_label = QLabel()
        self.layout.addWidget(self.coin_label)

        # Create buttons for all items
        for item_name, item_data in self.shop.items.items():

            button = QPushButton(
                f"{item_name.title()} - {item_data['price']} coins"
            )

            button.clicked.connect(
                lambda checked=False, name=item_name:
                self.buy_item(name)
            )

            self.layout.addWidget(button)

        self.setLayout(self.layout)

        self.refresh_ui()

    def refresh_ui(self):

        self.coin_label.setText(
            f"Coins: {self.pet.coin}"
        )

    def buy_item(self, item_name):

        success, message = self.shop.buy_item(
            self.pet,
            item_name
        )

        QMessageBox.information(
            self,
            "Shop",
            message
        )

        self.refresh_ui()
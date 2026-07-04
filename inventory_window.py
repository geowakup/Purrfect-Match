from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox
)

from shop_system import ShopSystem


class InventoryWindow(QWidget):

    def __init__(self, pet):

        super().__init__()

        self.pet = pet

        self.shop = ShopSystem()

        self.setWindowTitle("Inventory")

        self.resize(300, 400)

        self.layout = QVBoxLayout()

        self.coin_label = QLabel()

        self.layout.addWidget(
            self.coin_label
        )

        self.inventory_layout = QVBoxLayout()

        self.layout.addLayout(
            self.inventory_layout
        )

        self.setLayout(
            self.layout
        )

        self.refresh()

    def refresh(self):

        self.coin_label.setText(
            f"Coins: {self.pet.coins}"
        )

        while self.inventory_layout.count():

            child = (
                self.inventory_layout
                .takeAt(0)
            )

            if child.widget():

                child.widget().deleteLater()

        if not self.pet.inventory:

            self.inventory_layout.addWidget(
                QLabel(
                    "Inventory Empty"
                )
            )

            return

        for item in self.pet.inventory:

            btn = QPushButton(
                f"Use {item}"
            )

            btn.clicked.connect(
                lambda checked=False,
                name=item:
                self.use_item(name)
            )

            self.inventory_layout.addWidget(
                btn
            )

    def use_item(self, item):

        success, message = (
            self.shop.use_item(
                self.pet,
                item
            )
        )

        QMessageBox.information(
            self,
            "Inventory",
            message
        )

        self.refresh()
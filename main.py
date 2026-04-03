import sys
import json
from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap

# =========================
# PET LOGIC (Person 1)
# =========================
class Pet:
    def __init__(self):
        self.hunger = 100
        self.state = "happy"

    def update(self):
        self.hunger -= 1
        if self.hunger <= 30:
            self.state = "hungry"
        if self.hunger <= 0:
            self.hunger = 0
            self.state = "starving"

    def feed(self):
        self.hunger += 20
        if self.hunger > 100:
            self.hunger = 100
        self.state = "happy"


# =========================
# MAIN WINDOW (Person 2)
# =========================
class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Pet system
        self.pet = Pet()

        # Window setup
        self.setWindowTitle("Desktop Pet")
        self.setFixedSize(200, 200)

        # Make it look like a desktop pet
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Pet image
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 200, 200)

        # 👉 Replace with your own image later
        self.pixmap = QPixmap("pet.png")  
        self.label.setPixmap(self.pixmap)

        # Timer (game loop)
        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(1000)  # every 1 second

        # Drag support
        self.old_pos = None

    # =========================
    # GAME LOOP
    # =========================
    def game_loop(self):
        self.pet.update()
        print(f"Hunger: {self.pet.hunger}, State: {self.pet.state}")

    # =========================
    # CLICK = FEED PET
    # =========================
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pet.feed()
            print("Pet fed!")

        self.old_pos = event.globalPosition().toPoint()

    # =========================
    # DRAG WINDOW
    # =========================
    def mouseMoveEvent(self, event):
        if self.old_pos:
            delta = event.globalPosition().toPoint() - self.old_pos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.old_pos = event.globalPosition().toPoint()


# =========================
# MAIN APP
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PetWindow()
    window.show()

    sys.exit(app.exec())
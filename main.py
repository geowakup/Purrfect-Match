import sys
import os
import json
from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QPixmap, QMovie

# =========================
# PET LOGIC (Person 1)
# ========================
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

    def pet(self):
        self.is_being_petted = True

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
        self.movie = QMovie("happy.gif")  # your animation file
        self.label.setMovie(self.movie)
        self.movie.start()

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
        if self.pet.state == "happy":
            self.movie.setFileName("happy.gif")
        elif self.pet.state == "hungry":
            self.movie.setFileName("testing_1.gif")
        elif self.pet.state == "starving":
            self.movie.setFileName("testing_2.gif")
        elif self.pet.state == "petting":
            self.movie.setFileName("petting.gif")  # add this file

        self.movie.start()

    # =========================
    # CLICK = FEED PET
    # =========================
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.has_food():
                self.pet.feed()
            print("Pet fed!")
        else:
            self.pet.pet()
            print("Petting only (no food)")
            
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

#========================
# EXIT ON ESCAPE
#========================
class PetWindow(QWidget):
    def __init__(self):
        super().__init__()
        ...
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            QApplication.quit()

    def has_food(self):
        folder = "food"
        if not os.path.exists(folder):
            return False
        return len(os.listdir(folder)) > 0
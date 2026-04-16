import sys
import os
import json
import random
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
        self.action = None   

    def update(self):
        self.hunger -= 1

        if self.action:
            self.state = self.action
            self.action = None
            return

        if self.hunger <= 30:
            self.state = "hungry"
        if self.hunger <= 0:
            self.hunger = 0
            self.state = "starving"

    def pet(self):
        self.action = random.choice([
            "petting",
            "jump",
            "roll",
            "sleep"
        ])
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

        self.movie = QMovie("happy.gif")  
        self.label.setMovie(self.movie)
        self.movie.start()

        # Timer (game loop)
        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(1000)  # every 1 second

        # Drag support
        self.old_pos = None
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
    # =========================
    # GAME LOOP
    # =========================
    def game_loop(self):
        self.pet.update()
    
    state = self.pet.state

    if state == "happy":
        new_file = "happy.gif"
    elif state == "hungry":
        new_file = "hungry.gif"
    elif state == "starving":
        new_file = "starving.gif"
    elif state == "petting":
        new_file = "petting.gif"
    elif state == "jump":
        new_file = "jump.gif"
    elif state == "roll":
        new_file = "roll.gif"
    elif state == "sleep":
        new_file = "sleep.gif"
    else:
        new_file = "happy.gif"
    
    if self.movie.fileName() != new_file:
        self.movie.setFileName(new_file)
        self.movie.start()

    # =========================
    # CLICK = PET
    # =========================
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pet.pet()
            print("Pet interacted!")
            
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

    
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
        self.action_timer = 0   

    def update(self):
        self.hunger -= 1

        if self.action_timer > 0:
           self.state = self.action
           self.action_timer -= 1
           return

        if self.hunger <= 0:
           self.state = "starving"
        elif self.hunger <= 30:
           self.state = "hungry"
        else:
           self.state = "happy"

    def pet(self):
        self.action = random.choice([
            "petting",
            "jump",
            "roll",
            "sleep"
        ])
        self.action_timer = 3   
# =========================
# MAIN WINDOW (Person 2)
# =========================
class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.pet = Pet()

        self.setWindowTitle("Desktop Pet")
        self.setFixedSize(200, 200)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 200, 200)

        self.movie = QMovie("happy.gif")
        self.label.setMovie(self.movie)
        self.movie.start()

        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(1000)

        self.old_pos = None

    # ================= GAME LOOP =================
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

    # ================= DRAG + CLICK =================
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pet.pet()
            self.drag_pos = event.globalPosition().toPoint()
            
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()


    def mouseReleaseEvent(self, event):
        self.drag_pos = None
# =========================
# MAIN APP
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PetWindow()
    window.show()

    sys.exit(app.exec())

    
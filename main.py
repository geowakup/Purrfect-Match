import sys
import os
import random
from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtCore import Qt, QTimer
from PySide6.QtGui import QMovie
from PySide6.QtCore import QSize
from Todo import TodoApp

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

        self.label = QLabel(self)
        self.label.setAttribute(Qt.WA_TranslucentBackground)
        self.label.setStyleSheet("background: transparent;")
        
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.movie = QMovie(os.path.join(BASE_DIR, "happy.gif"))
        self.movie.setScaledSize(QSize(200, 200))
        self.label.setMovie(self.movie)
        self.movie.start()
        self.movie.frameChanged.connect(self.update_size)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(1000)

        self.drag_pos = None
        self.todo_window = None

    def update_size(self):
        self.resize(200, 200)
        self.label.setGeometry(0, 0, 200, 200)

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

            if self.todo_window is None:
                self.todo_window = TodoApp()
            self.todo_window.show()

            self.drag_pos = event.globalPosition().toPoint()
              
    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drag_pos is not None:
            current_pos = event.globalPosition().toPoint()
            delta = current_pos - self.drag_pos
            self.move(self.pos() + delta)
            self.drag_pos = current_pos
    
    def closeEvent(self, event):
        if self.todo_window is not None:
            self.todo_window.close()

        QApplication.quit()   
        event.accept()
# =========================
# MAIN APP
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = PetWindow()
    window.show()

    sys.exit(app.exec())
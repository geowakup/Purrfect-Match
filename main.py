import sys
import os
import random
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QPushButton
from PySide6.QtCore import Qt, QTimer, QSize
from PySide6.QtGui import QMovie
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

    #------------------------Window Titile + Transparent Background + Size------------------------
        self.setWindowTitle("Desktop Pet")

        self.label = QLabel(self)
        self.label.setAttribute(Qt.WA_TranslucentBackground)
        self.label.setStyleSheet("background: transparent;")
    
    #------------------------GIF Setup------------------------
    def update_size(self):
        self.resize(220, 240)
        self.label.setGeometry(0, 0, 200, 200)

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.current_gif = ""

        self.movie = QMovie(os.path.join(self.BASE_DIR, "firefly-hsr-firefly.gif"))
        print("GIF valid:", self.movie.isValid())
        self.movie.setScaledSize(QSize(200, 200))
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)

        self.label.setMovie(self.movie)
        self.movie.start()
        self.update_size()
        self.current_gif = os.path.join(self.BASE_DIR, "firefly-hsr-firefly.gif")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background: transparent;")

        self.timer = QTimer()
        self.timer.timeout.connect(self.game_loop)
        self.timer.start(200)

    #------------------------To-Do Button ------------------------
        self.todo_window = None
        self.drag_pos = None
       
        self.todo_button = QPushButton("To-Do", self)
        self.todo_button.setGeometry(60, 200, 100, 30)
        self.todo_button.clicked.connect(self.open_todo)

    def open_todo(self):
        if self.todo_window is None:
            self.todo_window = TodoApp()
        self.todo_window.show() 
        
    # ------------------------Game Loop: Update Pet State + Change GIF------------------------
    def game_loop(self):
        self.pet.update()

        state = self.pet.state

        if state == "happy":
            new_file = "firefly-hsr-firefly.gif"
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
        
        new_path = os.path.join(self.BASE_DIR, new_file)

        if self.current_gif != new_path:
            self.current_gif = new_path
            self.movie.stop()
            self.movie.setFileName(new_path)
            self.movie.start()

    # ------------------------Drag Window + Close App------------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.pet.pet()
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
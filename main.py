import sys
import os
import random
from timer_loop import TimerLoop 
from pet_lifecycle import PetLifecycle 
from pet import Pet 
from PySide6.QtWidgets import QApplication, QLabel, QWidget, QPushButton
from PySide6.QtCore import Qt, QTimer, QSize, QPropertyAnimation
from PySide6.QtGui import QMovie, QCursor
from Todo import TodoApp
from Setting import SettingsApp
from CharacterSelect import CharacterSelectApp
from advancement import AdvancementsManager
from styles import load_theme


# =========================
# MAIN WINDOW (Person 2)
# =========================
class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.pet = Pet()
        self.lifecycle = PetLifecycle(self.pet) 
        self.lifecycle.spawn()

        self.is_holding = False

        self.dragging = False

        self.settings_window = None

        self.todo_window = None

        self.drag_pos = None

        self.advancement_manager = AdvancementsManager()

        self.character_window = None
        
        self.current_character = "firefly"

# ---------------------------- Window setup ----------------------------
        self.setWindowTitle("Desktop Pet")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setStyleSheet("background: transparent; border:none;")

# ---------------------------- Label (GIF display) ----------------------------
        self.label = QLabel(self)
        self.label.setAttribute(Qt.WA_TranslucentBackground)
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents) 
        self.label.setStyleSheet("background: transparent;")

# ---------------------------- Size ----------------------------
        self.resize(220, 240)
        self.label.setGeometry(0, 0, 200, 200)

# ---------------------------- Paths ----------------------------
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.current_gif = ""

# ---------------------------- GIF setup ----------------------------
        self.movie = QMovie(os.path.join(self.BASE_DIR, "firefly_dance.gif"))
        print("GIF valid:", self.movie.isValid())

        self.movie.setScaledSize(QSize(200, 200))
        self.movie.setCacheMode(QMovie.CacheAll)
        self.movie.setSpeed(100)

        self.label.setMovie(self.movie)
        self.movie.start()

        self.current_gif = os.path.join(self.BASE_DIR, "firefly_dance.gif")

#---------------------------- Timer ----------------------------
        self.timer_loop = TimerLoop(
            self.pet,
            callback=self.game_loop,
            interval=200
        )

        self.timer_loop.start()
        

#---------------------------- Character Select Button ----------------------------
        self.character_button = QPushButton("Character", self)
        self.character_button.setGeometry(78, 200, 70, 30) 
        self.character_button.clicked.connect(self.open_character)

        self.character_button.setStyleSheet("""QPushButton {background-color: rgba(80, 200, 120, 220);color: white;border-radius: 10px;font-weight: bold;}QPushButton:hover {background-color: rgba(120, 230, 160, 255);}""")

        self.character_button.hide()

#---------------------------- To-Do Button ----------------------------
        self.todo_button = QPushButton("To-Do", self)
        self.todo_button.setGeometry(19, 200, 55, 30)
        self.todo_button.setFocusPolicy(Qt.StrongFocus)
        self.todo_button.clicked.connect(self.open_todo)

#---------------------------- Settings Button ----------------------------
        self.settings_button = QPushButton("Settings", self)
        self.settings_button.setGeometry(152, 200, 55, 30)  
        self.settings_button.setFocusPolicy(Qt.StrongFocus)
        self.settings_button.clicked.connect(self.open_settings)

        self.settings_button.setStyleSheet("""QPushButton {background-color: rgba(80, 80, 255, 220);color: white;border-radius: 10px;font-weight: bold;}QPushButton:hover {background-color: rgba(120, 120, 255, 255);}""")

        self.settings_button.hide()

# ------------------------ Button Hover + Style------------------
        self.hover_timer = QTimer()
        self.hover_timer.timeout.connect(self.check_hover)
        self.hover_timer.start(100)
        self.setMouseTracking(True)
        self.label.setMouseTracking(True)
        self.todo_button.setStyleSheet("""QPushButton {background-color: rgba(255, 80, 80, 220);color: white;border-radius: 10px;font-weight: bold;}QPushButton:hover {background-color: rgba(255, 120, 120, 255);}""")
        self.todo_button.hide() 

# ------------------------- Button Animation ------------------------
        self.anim = QPropertyAnimation(self.todo_button, b"windowOpacity")
        self.anim.setDuration(150)

# ------------------------- Button Hide Timer ------------------------
        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide_button)

# ------------------------- Hide Button Function ------------------------
    def hide_button(self):
        try:
            self.anim.finished.disconnect()
        except:
            pass

        self.anim.stop()
        self.anim.setStartValue(self.todo_button.windowOpacity())
        self.anim.setEndValue(0)

        self.anim.finished.connect(self.todo_button.hide)
        self.anim.finished.connect(self.settings_button.hide)
        self.anim.finished.connect(self.character_button.hide)
        self.anim.start()

# ------------------------ Check and trigger ------------------------
    def check_hover(self):
        local_pos = self.mapFromGlobal(QCursor.pos())
        hovered = self.label.geometry().contains(local_pos)

        if hovered and not self.todo_button.isVisible() :
            self.todo_button.show()
            self.settings_button.show()
            self.character_button.show()

            self.anim.stop()
            self.anim.setStartValue(self.todo_button.windowOpacity())
            self.anim.setEndValue(1)
            self.anim.start()
        
        if hovered:
            self.hide_timer.start(10000)
        else:
            if self.todo_button.isVisible() and not self.hide_timer.isActive():
                self.hide_timer.start(10000)

# ------------------------ Open To-Do Window ------------------------
    def open_todo(self):
        if self.todo_window is None or not self.todo_window.isVisible():
            self.todo_window = TodoApp()
            self.todo_window.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        self.todo_window.show()
        self.todo_window.raise_()
        self.todo_window.activateWindow() 

# ------------------------ Open Character Select Window ------------------------
    def open_character(self):
        if self.character_window is None or not self.character_window.isVisible():
            self.character_window = CharacterSelectApp()
            self.character_window.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        self.character_window.parent_window = self

        self.character_window.show()
        self.character_window.raise_()
        self.character_window.activateWindow()

#------------------------ Change Character (called from character select) ------------------------
    def change_character(self, name):
        self.current_character = name   
        
        if name == "firefly":
            file = "firefly_dance.gif"
        elif name == "cat":
            file = "cat_idle.gif"
        elif name == "dog":
            file = "dog_idle.gif"
        else:
            return

        new_path = os.path.join(self.BASE_DIR, file)

        if os.path.exists(new_path):
            self.current_gif = new_path
            self.movie.stop()
            self.movie.deleteLater()

            self.movie = QMovie(new_path)
            self.movie.setScaledSize(QSize(200, 200))
            self.label.setMovie(self.movie)
            self.movie.start()

# -------------------------- Setting --------------------------------------
    def open_settings(self):
        if self.settings_window is None or not self.settings_window.isVisible():
            self.settings_window = SettingsApp()
            self.settings_window.setWindowFlag(Qt.WindowStaysOnTopHint, True)

            self.settings_window.pet = self.pet
            self.settings_window.parent_window = self

            self.settings_window.show()
            self.settings_window.raise_()
            self.settings_window.activateWindow()

# ------------------------Game Loop: Update Pet State + Change GIF------------------------
    def game_loop(self):
        if self.is_holding and self.pet.hunger > 0:
            self.pet.action = "petting"
            self.pet.action_timer = 1  
        else:
            if self.pet.action == "petting":
                self.pet.action = None
                self.pet.action_timer = 0

        # Idle actions
        self.lifecycle.idle_behavior()

        # Death check
        if self.lifecycle.check_death():
            print("Pet died")

        # Update pet
        self.pet.update()
        
        if self.pet.hunger > 0:
            self.advancement_manager.add_progress("alive_1_hour",0.2)


        state = self.pet.state

        state_gifs = {
            "happy": f"{self.current_character}_idle.gif",
            "hungry": f"{self.current_character}_hungry.gif",
            "starving": f"{self.current_character}_starving.gif",
            "petting": f"{self.current_character}_petting.gif",
            "jump": f"{self.current_character}_jump.gif",
            "roll": f"{self.current_character}_roll.gif",
            "sleep": f"{self.current_character}_sleep.gif",

            # New moods
            "sleepy": f"{self.current_character}_sleep.gif",
            "dirty": f"{self.current_character}_idle.gif",
            "sad": f"{self.current_character}_hungry.gif",
        }

        new_file = state_gifs.get(
            state,
            f"{self.current_character}_idle.gif"
        )
        
        new_path = os.path.join(self.BASE_DIR, new_file)

        if not os.path.exists(new_path):
            print("Missing GIF:", new_path)
            return

        if self.current_gif != new_path:
            self.current_gif = new_path
            self.movie.stop()
            self.movie.deleteLater()
            self.movie = QMovie(new_path)
            self.movie.setScaledSize(QSize(200, 200))
            self.movie.setCacheMode(QMovie.CacheAll)
            self.movie.setSpeed(100)
            self.label.setMovie(self.movie)
            self.movie.start()

# ------------------------Drag Window + Close App------------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_holding = True
            self.drag_pos = event.globalPosition().toPoint()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_holding = False
            self.drag_pos = None
            self.dragging = False

            self.pet.action = None
            self.pet.action_timer = 0

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton and self.drag_pos is not None:
            current_pos = event.globalPosition().toPoint()
            delta = current_pos - self.drag_pos
            if delta.manhattanLength() > 3:
                self.dragging = True
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
    
    app.setStyleSheet(load_theme("pink"))
    window = PetWindow()
    window.show()

    sys.exit(app.exec())

    
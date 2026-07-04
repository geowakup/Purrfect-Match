import os
import sys
import random

from PySide6.QtCore import Qt, QPropertyAnimation, QTimer, QSize
from PySide6.QtGui import QMovie, QCursor, QPixmap
from shop_system import ShopSystem 
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QWidget

from CharacterSelect import CharacterSelectApp
from advancement import AdvancementsManager
from bgm import BGMPlayer
from cat import CatCharacter
from decoration import add_glow
from dog import DogCharacter
from firefly import FireflyCharacter
from pet import Pet
from pet_lifecycle import PetLifecycle
from save_system import SaveSystem
from timer_loop import TimerLoop
from styles import load_theme


# =========================
# MAIN WINDOW (Person 2)
# =========================
class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.pet = Pet()
        self.save_system = SaveSystem()
        self.current_character = "firefly"
        self.characters = {
            "firefly": FireflyCharacter(),
            "cat": CatCharacter(),
            "dog": DogCharacter()
        }
        self.current_asset_path = ""
        self.current_frame_paths = []
        self.current_frame_index = 0
        self.frame_timer = None
        self.movie = None
        self.current_frame_pixmaps = []
        self.drag_pos = None
        self.is_holding = False
        self.dragging = False
        self.inactivity_timer = None
        self._last_visual_state = None
        self.settings_window = None
        self.todo_window = None
        self.character_window = None
        self.advancement_manager = AdvancementsManager()
        
        # Developer Mode
        self.developer_mode = False

        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.ASSET_DIR = os.path.join(self.BASE_DIR, "assets", "images")
        self.bgm_player = BGMPlayer(self.BASE_DIR)

        self._load_saved_character()
        self.lifecycle = PetLifecycle(self.pet)
        if not self.loaded_character:
            self.lifecycle.spawn()
        
        # Set pet to idle state on startup
        self.pet.state = "idle"
        self.pet.action = None

        self._setup_window()self.shop_window = None
        self.inventory_window = None
        self._setup_label()
        self._setup_buttons()
        self._setup_timers()

        self.load_character_asset(self.current_character)
        self.bgm_player.stop()
        if self.bgm_player.has_tracks() and self._bgm_is_unlocked():
            self.bgm_player.play()

    def _load_saved_character(self):
        self.loaded_character = self.save_system.load_pet(self.pet)
        if self.loaded_character:
            self.current_character = self.loaded_character

    def _setup_window(self):
        self.setWindowTitle("Desktop Pet")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setStyleSheet("background: transparent; border:none;")

    def _bgm_is_unlocked(self):
        return (
            hasattr(self, "advancement_manager")
            and self.advancement_manager is not None
            and self.advancement_manager.has_feature_unlocked("bgm")
        )

    def _setup_label(self):
        self.label = QLabel(self)
        self.label.setAttribute(Qt.WA_TranslucentBackground)
        self.label.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.label.setStyleSheet("background: transparent;")
        self.resize(220, 240)
        self.label.setGeometry(0, 0, 200, 200)

    def _create_button(self, text, geometry, callback, stylesheet, hidden=True):
        button = QPushButton(text, self)
        button.setGeometry(*geometry)
        button.setFocusPolicy(Qt.StrongFocus)
        button.clicked.connect(callback)    
        button.setStyleSheet(stylesheet)
        if hidden:
            button.hide()
        return button

    def _setup_buttons(self):
        self.character_button = self._create_button(
            "Character",
            (78, 200, 70, 30),
            self.open_character,
            """
            QPushButton {
                background-color: rgba(80, 200, 120, 220);
                color: white;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(120, 230, 160, 255);
            }
            """
        )
        add_glow(self.character_button, "#7affb2")

        self.todo_button = self._create_button(
            "To-Do",
            (19, 200, 55, 30),
            self.open_todo,
            """
            QPushButton {
                background-color: rgba(255, 80, 80, 220);
                color: white;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(255, 120, 120, 255);
            }
            """
        )
        add_glow(self.todo_button)

        self.settings_button = self._create_button(
            "Settings",
            (152, 200, 55, 30),
            self.open_settings,
            """
            QPushButton {
                background-color: rgba(80, 80, 255, 220);
                color: white;
                border-radius: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: rgba(120, 120, 255, 255);
            }
            """
        )
        add_glow(self.settings_button, "#7aa2ff")

# ---------------------------- Shop Button ----------------------------
        self.shop_button = QPushButton("Shop", self)

        self.shop_button.setGeometry(78, 160, 70, 30)

        self.shop_button.clicked.connect(
            self.open_shop
        )

        self.shop_button.setStyleSheet("""
        QPushButton {
            background-color: rgba(255,180,0,220);
            color:white;
            border-radius:10px;
            font-weight:bold;
        }

        QPushButton:hover {
            background-color: rgba(255,210,80,255);
        }
        """)

        add_glow(self.shop_button, "#ffb24d")

        self.shop_button.hide()

# ---------------------------- Inventory Button ----------------------------
        self.inventory_button = QPushButton(
            "Inventory",
            self
        )

        self.inventory_button.setGeometry(60, 110, 100, 30)

        self.inventory_button.clicked.connect(
            self.open_inventory
        )

        self.inventory_button.setStyleSheet("""
        QPushButton{
        background-color: rgba(140,100,255,220);
        color:white;
        border-radius:10px;
        font-weight:bold;
        }

        QPushButton:hover{
        background-color: rgba(180,150,255,255);
        }
        """)

        add_glow(self.inventory_button, "#aa88ff")

        self.inventory_button.hide()

    def _setup_timers(self):
        self.hover_timer = QTimer()
        self.hover_timer.timeout.connect(self.check_hover)
        self.hover_timer.start(100)
        self.setMouseTracking(True)
        self.label.setMouseTracking(True)
        
        # Inactivity timer for sleep (30 seconds)
        self.inactivity_timer = QTimer()
        self.inactivity_timer.timeout.connect(self.trigger_sleep)
        self.inactivity_timer.start(30000)  # 30 seconds

        self.anim = QPropertyAnimation(self.todo_button, b"windowOpacity")
        self.anim.setDuration(150)

        self.hide_timer = QTimer(self)
        self.hide_timer.setSingleShot(True)
        self.hide_timer.timeout.connect(self.hide_button)

        self.timer_loop = TimerLoop(
            self.pet,
            callback=self.game_loop,
            interval=200
        )
        self.timer_loop.start()

    def _stop_frame_animation(self):
        if self.frame_timer is not None:
            try:
                self.frame_timer.stop()
            except Exception:
                pass
            self.frame_timer.deleteLater()
            self.frame_timer = None

        self.current_frame_paths = []
        self.current_frame_index = 0
        self.current_frame_pixmaps = []

    def _show_frame(self, index):
        if not self.current_frame_paths:
            return

        # Prefer preloaded pixmaps if available
        if self.current_frame_pixmaps:
            pixmap = self.current_frame_pixmaps[index]
            self.label.setPixmap(pixmap)
            return

        path = self.current_frame_paths[index]
        pixmap = QPixmap(path)
        if pixmap.isNull():
            print("Failed to load frame:", path)
            return

        pixmap = pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

    def _next_frame(self):
        if not self.current_frame_paths:
            return

        old = self.current_frame_index
        self.current_frame_index = (self.current_frame_index + 1) % len(self.current_frame_paths)
        print(f"Frame tick: {old} -> {self.current_frame_index}")
        self._show_frame(self.current_frame_index)

    def set_character_image(self, filename):
        if isinstance(filename, (list, tuple)):
            paths = [os.path.join(self.ASSET_DIR, frame) for frame in filename]

            for path in paths:
                if not os.path.exists(path):
                    print("Missing frame:", path)
                    return

            if self.movie is not None:
                try:
                    self.movie.stop()
                except Exception:
                    pass
                self.movie = None
                self.label.setMovie(None)

            self._stop_frame_animation()
            self.current_frame_paths = paths
            self.current_asset_path = tuple(paths)
            self.current_frame_index = 0

            # Preload and scale pixmaps for smoother animation
            pixmaps = []
            for p in paths:
                pm = QPixmap(p)
                if pm.isNull():
                    print("Failed to load frame:", p)
                    return
                pm = pm.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
                pixmaps.append(pm)

            self.current_frame_pixmaps = pixmaps
            self._show_frame(0)

            print(f"Starting frame animation: {len(paths)} frames for state {self.pet.action or self.pet.state}")
            self.frame_timer = QTimer(self)
            self.frame_timer.timeout.connect(self._next_frame)
            self.frame_timer.setInterval(250)
            self.frame_timer.start()
            print("Frame timer started")
            return

        path = os.path.join(self.ASSET_DIR, filename)

        if not os.path.exists(path):
            print("Missing image:", path)
            return

        self._stop_frame_animation()

        if self.movie is not None:
            try:
                self.movie.stop()
            except Exception:
                pass
            self.movie = None
            self.label.setMovie(None)

        self.current_asset_path = path
        ext = os.path.splitext(path)[1].lower()

        if ext == ".gif":
            self.movie = QMovie(path)
            self.movie.setScaledSize(QSize(350, 350))
            self.movie.setCacheMode(QMovie.CacheAll)
            self.movie.setSpeed(100)
            self.label.setMovie(self.movie)
            self.movie.start()
            return

        pixmap = QPixmap(path)
        if pixmap.isNull():
            print("Failed to load image:", path)
            return

        pixmap = pixmap.scaled(350, 350, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.label.setPixmap(pixmap)

    def load_character_asset(self, character_name=None):
        if character_name is None:
            character_name = self.current_character

        character = self.characters.get(character_name)
        if character is None:
            return

        state = self.pet.action or self.pet.state
        filename = character.get_file(state)

        if isinstance(filename, (list, tuple)):
            asset_key = tuple(filename)
        else:
            asset_key = os.path.join(self.ASSET_DIR, filename)

        # Update the displayed asset when the asset key changes
        # or when the visual state (action/state) changes so animations restart.
        if self.current_asset_path != asset_key or self._last_visual_state != state:
            self.set_character_image(filename)
            self._last_visual_state = state
        else:
            # Restart frame timer if animation asset is already loaded but timer stopped
            if isinstance(filename, (list, tuple)) and (
                self.frame_timer is None or not self.frame_timer.isActive()
            ):
                self.set_character_image(filename)
                self._last_visual_state = state

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
        self.anim.finished.connect(self.shop_button.hide)
        self.anim.finished.connect(self.inventory_button.hide)   
        self.anim.start()

# ------------------------ Check and trigger ------------------------
    def check_hover(self):
        local_pos = self.mapFromGlobal(QCursor.pos())
        hovered = self.label.geometry().contains(local_pos)

        if hovered and not self.todo_button.isVisible() :
            self.todo_button.show()
            self.settings_button.show()
            self.character_button.show()
            self.shop_button.show()
            self.inventory_button.show()

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
        self.character_window.refresh_feature_access()

        self.character_window.show()
        self.character_window.raise_()
        self.character_window.activateWindow()

# ------------------------
# Open Shop Window
# ------------------------
    def open_shop(self):

        if self.shop_window is None or not self.shop_window.isVisible():

            self.shop_window = ShopWindow(self.pet)

            self.shop_window.setWindowFlag(
                Qt.WindowStaysOnTopHint,
                True
            )

        self.shop_window.show()
        self.shop_window.raise_()
        self.shop_window.activateWindow()

# ------------------------
# Open Inventory Window
# ------------------------
    def open_inventory(self):

        if (
            self.inventory_window is None
            or not self.inventory_window.isVisible()
        ):

            self.inventory_window = (
                InventoryWindow(
                    self.pet
                )
            )

            self.inventory_window.setWindowFlag(
                Qt.WindowStaysOnTopHint,
                True
            )

        self.inventory_window.refresh()

        self.inventory_window.show()

        self.inventory_window.raise_()

        self.inventory_window.activateWindow()

#------------------------ Change Character (called from character select) ------------------------
    def change_character(self, name):
        self.current_character = name
        self.current_asset_path = ""
        self.load_character_asset(name)

# -------------------------- Setting --------------------------------------
    def open_settings(self):
        if self.settings_window is None or not self.settings_window.isVisible():
            self.settings_window = SettingsApp()
            self.settings_window.setWindowFlag(Qt.WindowStaysOnTopHint, True)

        self.settings_window.pet = self.pet
        self.settings_window.parent_window = self
        self.settings_window.refresh_feature_access()
        self.settings_window.load_quests()
        self.settings_window.update_coin_label()
        if hasattr(self.settings_window, "update_bgm_status"):
            self.settings_window.update_bgm_status()
        if hasattr(self.settings_window, "populate_bgm_tracks"):
            self.settings_window.populate_bgm_tracks()

        self.settings_window.show()
        self.settings_window.raise_()
        self.settings_window.activateWindow()

# ------------------------Game Loop: Update Pet State + Change GIF------------------------
    def game_loop(self):
        # If in developer mode, skip normal game updates
        if self.developer_mode:
            # Keep action running continuously for smooth looping
            if self.pet.action is not None:
                self.pet.action_timer = 100  # Keep action active indefinitely
            # Just update the visual state to reflect current pet state/action
            self.load_character_asset()
            return

        # Normal gameplay loop (disabled in developer mode)
        # Keep action timers high for smooth continuous 4-frame animation
        if self.pet.action is not None:
            self.pet.action_timer = max(self.pet.action_timer, 50)  # Maintain smooth animation
        
        # ---------------- Petting ----------------
        if self.is_holding and self.pet.hunger > 0:
            self.pet.action = "petting"
            self.pet.action_timer = 50  # Smooth continuous petting animation
        elif self.pet.action == "petting":
            # Keep petting action running smoothly
            self.pet.action_timer = max(self.pet.action_timer, 50)

        # Keep random action animations running smoothly
        if self.pet.action in ["jump", "roll", "happy", "sleep"]:
            self.pet.action_timer = max(self.pet.action_timer, 50)

        # ---------------- Idle Behavior ----------------
        self.lifecycle.idle_behavior()

        # ---------------- Death Check ----------------
        if self.lifecycle.check_death():
            print("Pet died")
            return

        # ---------------- Achievement Progress ----------------
        if self.pet.hunger > 0:
            self.advancement_manager.add_progress("alive_1_hour", 0.2)

        # ---------------- Current Visual State ----------------
        self.load_character_asset()

# ------------------------Sleep on Inactivity------------------------
    def trigger_sleep(self):
        """Trigger sleep state if no interaction for 30 seconds"""
        if self.pet.action is None and self.pet.state != "sleep":
            self.pet.action = "sleep"
            self.pet.action_timer = 50  # Increased for smooth looping

# ------------------------Drag Window + Close App------------------------
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_holding = True
            self.drag_pos = event.globalPosition().toPoint()
    
    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.is_holding = False
            
            # If it wasn't a drag, trigger a random action
            if not self.dragging:
                self.pet.action = random.choice(["happy", "jump", "petting", "roll"])
                self.pet.action_timer = 50  # Increased for smooth looping
                # Reset inactivity timer on interaction
                self.inactivity_timer.stop()
                self.inactivity_timer.start(30000)
            else:
                self.pet.action = None
                self.pet.action_timer = 0
            
            self.drag_pos = None
            self.dragging = False

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
    # Developer Mode Methods
    # =========================
    def enter_developer_mode(self):
        """Enter developer mode - stops normal game loop updates"""
        self.developer_mode = True
        print("Developer Mode: ENABLED - All normal game updates paused")
        # Stop normal update timers and freeze pet stats
        self.inactivity_timer.stop()
        if self.timer_loop is not None:
            self.timer_loop.stop()
        self.pet.alive = True
        self.pet.hunger = max(0, self.pet.hunger)
        self.pet.energy = max(0, self.pet.energy)
        self.pet.happiness = max(0, self.pet.happiness)
        self.pet.cleanliness = max(0, self.pet.cleanliness)
        self.pet.action_timer = 9999
    
    def exit_developer_mode(self):
        """Exit developer mode - resume normal game loop"""
        self.developer_mode = False
        print("Developer Mode: DISABLED - Resuming normal gameplay")
        # Reset developer mode overrides so pet stats can resume updating
        self.pet.action = None
        self.pet.action_timer = 0
        self.pet.update_state()
        # Force reload of the current animation so normal cycling restarts
        self._last_visual_state = None
        self.load_character_asset()
        # Resume normal timers
        self.inactivity_timer.start(30000)
        if self.timer_loop is not None:
            self.timer_loop.start()
# =========================
# MAIN APP
# =========================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    app.setStyleSheet(load_theme("pink"))
    window = PetWindow()
    window.show()

    sys.exit(app.exec())


import os
import sys
import random

from PySide6.QtCore import Qt, QPropertyAnimation, QTimer, QSize
from PySide6.QtGui import QMovie, QCursor, QPixmap, QShortcut, QKeySequence
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QWidget, QMessageBox

from CharacterSelect import CharacterSelectApp
from advancement import AdvancementsManager
from bgm import BGMPlayer
from cat import CatCharacter
from decoration import add_glow
from dog import DogCharacter
from firefly import FireflyCharacter
from inventory_window import InventoryWindow
from pet import Pet
from pet_lifecycle import PetLifecycle
from save_system import SaveSystem
from Setting import SettingsApp
from shop_system import ShopSystem
from shop_window import ShopWindow
from styles import load_theme
from timer_loop import TimerLoop
from Todo import TodoApp


# =========================
# MAIN WINDOW (Person 2)
# =========================
class PetWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.pet = Pet()
        self.pet.save_callback = self.persist_pet_state
        self.pet.advancement_callback = self.handle_advancement_progress
        self.save_system = SaveSystem()
        self.current_character = "firefly"
        self.characters = {
            "firefly": FireflyCharacter(),
            "cat": CatCharacter(),
            "dog": DogCharacter(),
            "river_flow_to_you": FireflyCharacter(),
            "summer_ghost": FireflyCharacter()
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
        # ensure rewards can be delivered back to the main window
        self.advancement_manager.reward_callback = self.reward_player_with_coins
        
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

        self._setup_window()
        self.shop_window = None
        self.inventory_window = None
        self._setup_label()

        self.unlock_shortcut = QShortcut(QKeySequence("Ctrl+Shift+D"), self)
        self.unlock_shortcut.activated.connect(self.unlock_all_features)
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
        """Advance through the current animation sequence and stop after the final frame."""
        if not self.current_frame_paths:
            return

        if not self.frame_timer or not self.frame_timer.isActive():
            self.frame_timer = QTimer(self)
            self.frame_timer.timeout.connect(self._next_frame)
            self.frame_timer.setInterval(250)  # 250ms per frame
            self.frame_timer.start()
            return

        next_index = self.current_frame_index + 1
        if next_index >= len(self.current_frame_paths):
            self._show_frame(self.current_frame_index)
            self._stop_frame_animation()
            print(f"Animation finished for state {self.pet.action or self.pet.state}")
            return

        self.current_frame_index = next_index
        print(f"Frame {self.current_frame_index + 1}/{len(self.current_frame_paths)}: {self.current_frame_paths[self.current_frame_index]}")
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
            print(f"Initial: showing frame index 0: {paths[0]}")
            print(f"Starting frame animation: {len(paths)} frames for state {self.pet.action or self.pet.state}")
            self.frame_timer = QTimer(self)
            self.frame_timer.timeout.connect(self._next_frame)
            self.frame_timer.setInterval(250)  # 250ms per frame
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

        # Only switch visuals once the current animation cycle has fully finished.
        # This makes all states wait for the full four-frame loop before the next state starts.
        is_animation_playing = (
            self.frame_timer is not None
            and self.frame_timer.isActive()
        )

        should_restart = False

        if self.current_asset_path != asset_key:
            if not is_animation_playing:
                should_restart = True
        elif not is_animation_playing and self._last_visual_state != state:
            should_restart = True

        if should_restart:
            print(f"Starting animation for state {state}")
            self.set_character_image(filename)
            self._last_visual_state = state

# ------------------------- Hide Button Function ------------------------
    def hide_button(self):
        if not self.todo_button.isVisible():
            return

        self.todo_button.hide()
        self.settings_button.hide()
        self.character_button.hide()

# ------------------------ Check and trigger ------------------------
    def check_hover(self):
        local_pos = self.mapFromGlobal(QCursor.pos())
        hovered = (
            self.label.geometry().contains(local_pos)
            or self.character_button.geometry().contains(local_pos)
            or self.todo_button.geometry().contains(local_pos)
            or self.settings_button.geometry().contains(local_pos)
        )

        if hovered:
            self.hide_timer.stop()
            if not self.todo_button.isVisible():
                self.todo_button.show()
                self.settings_button.show()
                self.character_button.show()
            return

        if self.todo_button.isVisible() and not self.hide_timer.isActive():
            self.hide_timer.start(5000)

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
# Open Inventory Window
# ------------------------
#------------------------ Change Character (called from character select) ------------------------
    def change_character(self, name):
        self.current_character = name
        self.current_asset_path = ""
        self.load_character_asset(name)
        self.play_character_music(name)

    def play_character_music(self, character_name):
        if not hasattr(self, "bgm_player") or self.bgm_player is None:
            return

        track_map = {
            "river_flow_to_you": "river flows to you.MP3",
            "summer_ghost": "summer_ghost.MP3",
        }

        track_name = track_map.get(character_name)
        if not track_name:
            return

        if self.bgm_player.load_track(track_name):
            self.bgm_player.play()

            if (
                hasattr(self, "settings_window")
                and self.settings_window is not None
                and hasattr(self.settings_window, "update_bgm_status")
            ):
                self.settings_window.update_bgm_status()

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

    def persist_pet_state(self):
        if hasattr(self, "save_system") and self.save_system is not None and self.pet is not None:
            self.save_system.save_pet(self.pet, self.current_character)

    def handle_advancement_progress(self, key):
        if hasattr(self, "advancement_manager") and self.advancement_manager is not None:
            self.advancement_manager.add_progress(key)

    def reward_player_with_coins(self, amount):
        if self.pet is not None:
            self.pet.coins += amount
            self.persist_pet_state()
            if hasattr(self, "settings_window") and self.settings_window is not None:
                self.settings_window.update_coin_label()

    def unlock_all_features(self):
        if not hasattr(self, "advancement_manager") or self.advancement_manager is None:
            return

        manager = self.advancement_manager

        for feature_name in [
            "dark_theme",
            "cyber_theme",
            "bgm",
            "developer_mode",
            "river_flow",
            "summer_ghost",
        ]:
            manager.feature_unlocks[feature_name] = True

        for advancement in manager.advancements.values():
            advancement["unlocked"] = True

        manager.save_data()
        manager.sync_feature_unlocks()

        if self.settings_window is not None:
            self.settings_window.refresh_feature_access()
            self.settings_window.update_coin_label()
            self.settings_window.refresh_inventory()
            if hasattr(self.settings_window, "update_bgm_status"):
                self.settings_window.update_bgm_status()
            if hasattr(self.settings_window, "populate_bgm_tracks"):
                self.settings_window.populate_bgm_tracks()

        if hasattr(self, "settings_window") and self.settings_window is not None:
            self.settings_window.developer_mode = True
            self.settings_window.show_dev_controls()
            self.settings_window.dev_mode_toggle.setChecked(True)
            self.settings_window.dev_mode_toggle.setText("Disable Developer Mode")

        if hasattr(self, "enter_developer_mode"):
            self.enter_developer_mode()

        QMessageBox.information(self, "Unlock All", "All features and developer tools have been unlocked.")

# ------------------------Game Loop: Update Pet State + Change GIF------------------------
    def game_loop(self):
        # If in developer mode, skip normal game updates
        if self.developer_mode:
            # Keep action running continuously for smooth looping
            if self.pet.action is not None:
                self.pet.action_timer = 200  # Keep action active indefinitely
            # Just update the visual state to reflect current pet state/action
            self.load_character_asset()
            return

        # Normal gameplay loop (disabled in developer mode)
        # Use EXACT same action maintenance as developer mode
        if self.pet.action is not None:
            self.pet.action_timer = 200  # Keep action running indefinitely (same as dev mode)
        
        # Keep holding down for petting action
        if self.is_holding and self.pet.hunger > 0:
            self.pet.action = "petting"
            self.pet.action_timer = 200

        # ---------------- Idle Behavior ----------------
        self.lifecycle.idle_behavior()

        # ---------------- Death Check ----------------
        if self.lifecycle.check_death():
            print("Pet died")
            return

        # ---------------- Achievement Progress ----------------
        if self.pet.hunger > 0:
            self.advancement_manager.add_progress("play_for_1_hour", 0.2)

        # ---------------- Current Visual State ----------------
        self.load_character_asset()

# ------------------------Sleep on Inactivity------------------------
    def trigger_sleep(self):
        """Trigger sleep state if no interaction for 30 seconds"""
        if self.pet.action is None and self.pet.state != "sleep":
            self.pet.action = "sleep"
            self.pet.action_timer = 200  # Keep animation looping

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
                self.pet.action_timer = 200  # Keep animation looping
                if hasattr(self, "advancement_manager") and self.advancement_manager is not None:
                    self.advancement_manager.add_progress("click_pet")
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

        try:
            self.persist_pet_state()
        except Exception as exc:
            print(f"Failed to save pet on close: {exc}")

        if hasattr(self, "advancement_manager") and self.advancement_manager is not None:
            try:
                # persist advancement progress and synced feature flags
                self.advancement_manager.save_data()
                self.advancement_manager.sync_feature_unlocks()
            except Exception as exc:
                print(f"Failed to save advancement on close: {exc}")

        QApplication.quit()
        event.accept()

    def reset_all_saves(self):
        """Delete all save files in the data folder and reset advancements to defaults."""
        try:
            base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
            targets = [
                os.path.join(base, "save_data.json"),
                os.path.join(base, "advancement.json"),
                os.path.join(base, "pet.json"),
                os.path.join(base, "quests.json"),
                os.path.join(base, "stats.json"),
                os.path.join(base, "tasks.json"),
            ]
            for path in targets:
                if os.path.exists(path):
                    try:
                        os.remove(path)
                    except OSError:
                        pass

            # Also try legacy save at repository root
            legacy = os.path.join(os.path.dirname(os.path.abspath(__file__)), "save_data.json")
            if os.path.exists(legacy):
                try:
                    os.remove(legacy)
                except OSError:
                    pass

            # Reset in-memory advancement manager to defaults and persist
            if hasattr(self, "advancement_manager") and self.advancement_manager is not None:
                defaults = self.advancement_manager._build_default_advancements()
                self.advancement_manager.advancements = defaults
                self.advancement_manager._sync_advancement_list()
                self.advancement_manager.sync_feature_unlocks()
                self.advancement_manager.save_data()

            # Reset pet save via SaveSystem
            if hasattr(self, "save_system") and self.save_system is not None:
                try:
                    if os.path.exists(self.save_system.filename):
                        os.remove(self.save_system.filename)
                except OSError:
                    pass

            # Refresh UI state if settings window open
            if hasattr(self, "settings_window") and self.settings_window is not None:
                self.settings_window.refresh_feature_access()
                self.settings_window.update_coin_label()
                self.settings_window.refresh_inventory()

            print("All save data cleared and advancements reset to defaults.")
        except Exception as exc:
            print(f"Failed to reset saves: {exc}")
    
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
        self.pet.happiness = max(0, self.pet.happiness)
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


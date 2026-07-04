from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QSlider,
    QMessageBox,
    QInputDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QKeySequence, QShortcut
from PySide6.QtMultimedia import QMediaPlayer
from shop_system import ShopSystem
from styles import load_theme
from system.quest_system import QuestSystem


# =========================
# Settings
# =========================
class SettingsApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Settings")
        self.resize(300, 450)

        layout = QVBoxLayout()
        
        #=========================
        # Theme Button
        #=========================
        self.pink_theme_btn = QPushButton("Pink Theme")
        self.dark_theme_btn = QPushButton("🔒 Dark Theme")
        self.cyber_theme_btn = QPushButton("🔒 Cyber Theme")

        layout.addWidget(self.pink_theme_btn)
        layout.addWidget(self.dark_theme_btn)
        layout.addWidget(self.cyber_theme_btn)
        self.dark_theme_btn.setEnabled(False)
        self.cyber_theme_btn.setEnabled(False)

        self.pink_theme_btn.clicked.connect(
        lambda: self.change_theme("pink")
        )

        self.dark_theme_btn.clicked.connect(
        lambda: self.change_theme("dark")
        )

        self.cyber_theme_btn.clicked.connect(
        lambda: self.change_theme("cyber")
        )


        # =========================
        # Advancement Button
        # =========================
        self.advancement_button = QPushButton("Advancements")
        self.advancement_button.clicked.connect(self.show_advancements)
        layout.addWidget(self.advancement_button)

        # =========================
        # Shop Button
        # =========================
        self.shop_button = QPushButton("Open Shop")
        self.shop_button.clicked.connect(self.open_shop)
        layout.addWidget(self.shop_button)

        self.shop_system = ShopSystem()

        self.inventory_panel = QWidget(self)
        self.inventory_panel.setStyleSheet("""
        QWidget {
            background-color: rgba(140, 100, 255, 220);
            color: white;
            border-radius: 10px;
            padding: 6px;
        }
        QPushButton {
            background-color: rgba(255, 255, 255, 220);
            color: #4b2b8f;
            border-radius: 6px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 255);
        }
        """)

        self.inventory_panel_layout = QVBoxLayout(self.inventory_panel)
        self.inventory_panel_layout.setContentsMargins(8, 8, 8, 8)
        self.inventory_panel_layout.setSpacing(6)

        self.inventory_label = QLabel("Inventory")
        self.inventory_label.setStyleSheet("font-weight: bold; color: white;")
        self.inventory_panel_layout.addWidget(self.inventory_label)

        self.inventory_layout = QVBoxLayout()
        self.inventory_layout.setSpacing(4)
        self.inventory_panel_layout.addLayout(self.inventory_layout)
        self.inventory_widgets = []
        layout.addWidget(self.inventory_panel)

        self.coins_label = QLabel("Coins: 0")
        layout.addWidget(self.coins_label)

        self.quest_title = QLabel("Daily Quests")
        layout.addWidget(self.quest_title)

        self.quest_layout = QVBoxLayout()
        self.quest_labels = []
        layout.addLayout(self.quest_layout)

        self.refresh_quests_button = QPushButton("Refresh Quests")
        self.refresh_quests_button.clicked.connect(self.load_quests)
        layout.addWidget(self.refresh_quests_button)

        self.quest_system = QuestSystem()

        self.river_flow_button = QPushButton("🔒 River Flow to You")
        self.river_flow_button.clicked.connect(lambda: self.select_character("river_flow_to_you"))
        self.river_flow_button.setEnabled(False)
        layout.addWidget(self.river_flow_button)

        self.summer_ghost_button = QPushButton("🔒 Summer Ghost")
        self.summer_ghost_button.clicked.connect(lambda: self.select_character("summer_ghost"))
        self.summer_ghost_button.setEnabled(False)
        layout.addWidget(self.summer_ghost_button)

        # =========================
        # Hidden Golden Finger Buttons
        # =========================
        self.feed_button = QPushButton("Feed Pet (+20 hunger)")
        self.feed_button.clicked.connect(self.feed_pet)
        self.feed_button.hide()
        layout.addWidget(self.feed_button)

        self.play_button = QPushButton("Play Action")
        self.play_button.clicked.connect(self.play_action)
        self.play_button.hide()
        layout.addWidget(self.play_button)

        # =========================
        # Background Music Controls
        # =========================
        self.bgm_label = QLabel("Background Music Volume: 100")
        layout.addWidget(self.bgm_label)
        self.bgm_label.setEnabled(False)

        self.bgm_slider = QSlider(Qt.Horizontal)
        self.bgm_slider.setRange(0, 100)
        self.bgm_slider.setValue(100)
        self.bgm_slider.valueChanged.connect(self.change_bgm_volume)
        layout.addWidget(self.bgm_slider)
        self.bgm_slider.setEnabled(False)

        self.bgm_status_label = QLabel("🔒 BGM Locked")
        layout.addWidget(self.bgm_status_label)

        # BGM Track Selection
        self.bgm_tracks_label = QLabel("🔒 Select BGM Track:")
        layout.addWidget(self.bgm_tracks_label)
        self.bgm_tracks_layout = QHBoxLayout()
        self.bgm_tracks_placeholder = QLabel("🔒 Locked until BGM is unlocked")
        self.bgm_tracks_placeholder.setEnabled(False)
        self.bgm_tracks_layout.addWidget(self.bgm_tracks_placeholder)
        self.bgm_tracks_buttons = {}
        layout.addLayout(self.bgm_tracks_layout)
        self.bgm_tracks_layout.setContentsMargins(0, 0, 0, 0)

        self.bgm_button_layout = QHBoxLayout()
        self.bgm_play_button = QPushButton("🔒 Play BGM")
        self.bgm_play_button.clicked.connect(self.play_bgm)
        self.bgm_button_layout.addWidget(self.bgm_play_button)
        self.bgm_play_button.setEnabled(False)

        self.bgm_stop_button = QPushButton("🔒 Stop BGM")
        self.bgm_stop_button.clicked.connect(self.stop_bgm)
        self.bgm_button_layout.addWidget(self.bgm_stop_button)
        self.bgm_stop_button.setEnabled(False)

        layout.addLayout(self.bgm_button_layout)

        # =========================
        # Developer Mode Section
        # =========================
        self.dev_mode_label = QLabel("🔒 Developer Mode")
        layout.addWidget(self.dev_mode_label)
        self.dev_mode_label.setEnabled(False)
        
        self.dev_mode_toggle = QPushButton("🔒 Enable Developer Mode")
        self.dev_mode_toggle.setCheckable(True)
        self.dev_mode_toggle.clicked.connect(self.toggle_developer_mode)
        layout.addWidget(self.dev_mode_toggle)
        self.dev_mode_toggle.setEnabled(False)
        
        # States selector
        self.states_label = QLabel("Select State:")
        self.states_label.hide()
        layout.addWidget(self.states_label)
        
        self.states_layout = QHBoxLayout()
        self.state_buttons = {}
        layout.addLayout(self.states_layout)
        
        # Actions selector
        self.actions_label = QLabel("Select Action:")
        self.actions_label.hide()
        layout.addWidget(self.actions_label)
        
        self.actions_layout = QHBoxLayout()
        self.action_buttons = {}
        layout.addLayout(self.actions_layout)
        
        # Exit dev mode button
        self.exit_dev_button = QPushButton("Exit Developer Mode")
        self.exit_dev_button.clicked.connect(self.exit_developer_mode)
        self.exit_dev_button.hide()
        layout.addWidget(self.exit_dev_button)

        self.refresh_feature_access()
        self.load_quests()

        self.setLayout(layout)

        self.pet = None
        self.developer_mode = False

        # =========================
        # Secret Shortcut
        # Ctrl + Shift + G
        # =========================
        self.secret_shortcut = QShortcut(
            QKeySequence("Ctrl+Shift+G"),
            self
        )
        self.secret_shortcut.activated.connect(
            self.toggle_golden_finger
        )

        self.golden_mode = False
    # =========================
    # Theme Change Function             
    # =========================
    def change_theme(self, theme_name):
        app = QApplication.instance()
        app.setStyleSheet(load_theme(theme_name))

    def _can_access_bgm(self):
        if self.developer_mode:
            return True

        if not hasattr(self, "parent_window") or self.parent_window is None:
            return False

        manager = getattr(self.parent_window, "advancement_manager", None)
        if manager is None:
            return False

        return manager.has_feature_unlocked("bgm")

    def refresh_feature_access(self):
        manager = None
        if hasattr(self, "parent_window") and self.parent_window is not None:
            manager = getattr(self.parent_window, "advancement_manager", None)

        if manager is None:
            return

        manager.sync_feature_unlocks()

        dark_unlocked = manager.has_feature_unlocked("dark_theme")
        cyber_unlocked = manager.has_feature_unlocked("cyber_theme")
        bgm_unlocked = self._can_access_bgm()
        dev_unlocked = manager.has_feature_unlocked("developer_mode")

        self.dark_theme_btn.setEnabled(dark_unlocked)
        self.cyber_theme_btn.setEnabled(cyber_unlocked)

        river_unlocked = manager.has_feature_unlocked("river_flow")
        summer_unlocked = manager.has_feature_unlocked("summer_ghost")

        self.river_flow_button.setEnabled(river_unlocked)
        self.river_flow_button.setText("River Flow to You" if river_unlocked else "🔒 River Flow to You")
        self.summer_ghost_button.setEnabled(summer_unlocked)
        self.summer_ghost_button.setText("Summer Ghost" if summer_unlocked else "🔒 Summer Ghost")

        # Keep the control buttons available permanently, but only allow actual song playback
        # once the achievement-based unlock is active.
        self.bgm_label.setEnabled(True)
        self.bgm_slider.setEnabled(True)
        self.bgm_status_label.setText("🔒 BGM Locked" if not bgm_unlocked else "🎵 BGM Unlocked")
        self.bgm_tracks_label.setText("🔒 Select BGM Track:" if not bgm_unlocked else "Select BGM Track:")
        self.bgm_tracks_label.setEnabled(True)
        self.bgm_play_button.setEnabled(True)
        self.bgm_stop_button.setEnabled(True)
        self.bgm_play_button.setText("Play BGM")
        self.bgm_stop_button.setText("Stop BGM")
        self.bgm_tracks_placeholder.setVisible(not bgm_unlocked)

        if bgm_unlocked:
            self.populate_bgm_tracks()
        else:
            self.clear_bgm_tracks()

        self.dev_mode_label.setText("🔒 Developer Mode" if not dev_unlocked else "Developer Mode")
        self.dev_mode_label.setEnabled(dev_unlocked)
        self.dev_mode_toggle.setText("🔒 Enable Developer Mode" if not dev_unlocked else "Enable Developer Mode")
        self.dev_mode_toggle.setEnabled(dev_unlocked)
        self.states_label.setVisible(dev_unlocked and self.developer_mode)
        self.actions_label.setVisible(dev_unlocked and self.developer_mode)
        self.exit_dev_button.setVisible(dev_unlocked and self.developer_mode)

        self.update_coin_label()
        self.refresh_inventory()
    # Advancement Window
    # =========================
    def show_advancements(self):
        advancement_text = (self.parent_window.advancement_manager.get_advancement_text())

        QMessageBox.information(self,"Advancements",advancement_text)

    # =========================
    # Golden Finger Toggle
    # =========================
    def toggle_golden_finger(self):
        self.golden_mode = not self.golden_mode

        self.feed_button.setVisible(self.golden_mode)
        self.play_button.setVisible(self.golden_mode)

        print("Golden Finger:", self.golden_mode)

    def update_coin_label(self):
        coins = self.pet.coins if self.pet else 0
        self.coins_label.setText(f"Coins: {coins}")

    def refresh_inventory(self):
        for widget in self.inventory_widgets:
            self.inventory_layout.removeWidget(widget)
            widget.deleteLater()
        self.inventory_widgets.clear()

        if self.pet is None:
            empty_label = QLabel("No pet data")
            self.inventory_layout.addWidget(empty_label)
            self.inventory_widgets.append(empty_label)
            return

        if not self.pet.inventory:
            empty_label = QLabel("Inventory empty")
            self.inventory_layout.addWidget(empty_label)
            self.inventory_widgets.append(empty_label)
            return

        for item_name in self.pet.inventory:
            item_button = QPushButton(f"Use {item_name}")
            item_button.clicked.connect(lambda checked=False, name=item_name: self.use_inventory_item(name))
            self.inventory_layout.addWidget(item_button)
            self.inventory_widgets.append(item_button)

    def use_inventory_item(self, item_name):
        if self.pet is None:
            QMessageBox.warning(self, "Inventory", "Pet data not available.")
            return

        success, message = self.shop_system.use_item(self.pet, item_name)
        if success and hasattr(self.parent_window, "advancement_manager"):
            self.parent_window.advancement_manager.add_progress("feed_pet")
        QMessageBox.information(self, "Inventory", message)
        self.update_coin_label()
        self.refresh_inventory()

    def load_quests(self):
        if not hasattr(self, "quest_system"):
            self.quest_system = QuestSystem()

        quests = self.quest_system.get_quests()

        for label in self.quest_labels:
            self.quest_layout.removeWidget(label)
            label.deleteLater()
        self.quest_labels.clear()

        for quest in quests:
            quest_text = f"{quest['progress']}/{quest['goal']} - {quest['name']}"
            label = QLabel(quest_text)
            label.setWordWrap(True)
            self.quest_layout.addWidget(label)
            self.quest_labels.append(label)

    def select_character(self, name):
        if not hasattr(self, "parent_window") or self.parent_window is None:
            QMessageBox.warning(self, "Character", "Character selection is not available.")
            return

        if not hasattr(self.parent_window, "advancement_manager"):
            QMessageBox.warning(self, "Character", "Advancement manager is not available.")
            return

        manager = self.parent_window.advancement_manager
        manager.sync_feature_unlocks()
        feature_name = "river_flow" if name == "river_flow_to_you" else "summer_ghost"
        if not manager.has_feature_unlocked(feature_name):
            QMessageBox.warning(self, "Character", "This character is locked.")
            return

        self.parent_window.change_character(name)

    # =========================
    # Pet Functions
    # =========================
    def feed_pet(self):
        if self.pet:
            self.pet.hunger = min(100,self.pet.hunger + 20)

        self.parent_window.advancement_manager.add_progress(
            "feed_pet"
        )
        self.refresh_feature_access()
    def play_action(self):
        if self.pet:
            self.pet.trigger_random_action()

            self.parent_window.advancement_manager.add_progress("click_pet")
            self.refresh_feature_access()

    # =========================
    # Volume Functions
    # =========================
    def change_bgm_volume(self, value):
        self.bgm_label.setText(
            f"Background Music Volume: {value}"
        )

        if hasattr(self, "parent_window") and self.parent_window is not None:
            if hasattr(self.parent_window, "bgm_player"):
                self.parent_window.bgm_player.set_volume(value)

    def play_bgm(self):
        if not hasattr(self, "parent_window") or self.parent_window is None:
            QMessageBox.warning(self, "BGM", "BGM controller not available.")
            return

        if not hasattr(self.parent_window, "advancement_manager"):
            QMessageBox.warning(self, "BGM", "BGM unlock manager not available.")
            return

        if not self._can_access_bgm():
            QMessageBox.information(self, "BGM", "No BGM track is unlocked yet.")
            return

        if not hasattr(self.parent_window, "bgm_player"):
            QMessageBox.warning(self, "BGM", "BGM player is not initialized.")
            return

        if not self.parent_window.bgm_player.has_tracks():
            QMessageBox.information(
                self,
                "BGM",
                "No audio files found in assets/audio. Add .mp3, .wav, .ogg or .flac files there."
            )
            return

        self.parent_window.bgm_player.play()
        self.update_bgm_status()

    def stop_bgm(self):
        if not hasattr(self, "parent_window") or self.parent_window is None:
            QMessageBox.warning(self, "BGM", "BGM controller not available.")
            return

        if not hasattr(self.parent_window, "advancement_manager"):
            QMessageBox.warning(self, "BGM", "BGM unlock manager not available.")
            return

        if not self._can_access_bgm():
            QMessageBox.information(self, "BGM", "No BGM track is unlocked yet.")
            return

        if not hasattr(self.parent_window, "bgm_player"):
            QMessageBox.warning(self, "BGM", "BGM player is not initialized.")
            return

        if not self.parent_window.bgm_player.has_tracks():
            QMessageBox.information(
                self,
                "BGM",
                "No audio files found in assets/audio. Add .mp3, .wav, .ogg or .flac files there."
            )
            return

        self.parent_window.bgm_player.stop()
        self.update_bgm_status()

    def update_bgm_status(self):
        if not hasattr(self, "parent_window") or self.parent_window is None:
            self.bgm_status_label.setText("BGM: Unknown")
            return

        if not hasattr(self.parent_window, "advancement_manager"):
            self.bgm_status_label.setText("BGM: Unknown")
            return

        bgm_unlocked = self._can_access_bgm()
        if not bgm_unlocked:
            self.bgm_status_label.setText("🔒 BGM Locked")
            self.bgm_play_button.setEnabled(True)
            self.bgm_stop_button.setEnabled(True)
            return

        if not hasattr(self.parent_window, "bgm_player"):
            self.bgm_status_label.setText("BGM: Not initialized")
            return

        player = self.parent_window.bgm_player
        if not player.has_tracks():
            self.bgm_status_label.setText("BGM: No tracks")
        elif player.player.playbackState() == QMediaPlayer.PlayingState:
            self.bgm_status_label.setText("BGM: Playing")
        else:
            self.bgm_status_label.setText("BGM: Stopped")

        self.bgm_play_button.setEnabled(player.player.playbackState() != QMediaPlayer.PlayingState)
        self.bgm_stop_button.setEnabled(player.player.playbackState() == QMediaPlayer.PlayingState)

    def clear_bgm_tracks(self):
        for btn in list(self.bgm_tracks_buttons.values()):
            self.bgm_tracks_layout.removeWidget(btn)
            btn.deleteLater()
        self.bgm_tracks_buttons.clear()

    def populate_bgm_tracks(self):
        """Populate track selection buttons from available BGM tracks"""
        if not hasattr(self, "parent_window") or self.parent_window is None:
            return

        if not hasattr(self.parent_window, "advancement_manager"):
            return

        if not self._can_access_bgm():
            self.clear_bgm_tracks()
            self.bgm_tracks_placeholder.setVisible(True)
            return

        self.bgm_tracks_placeholder.setVisible(False)

        if not hasattr(self.parent_window, "bgm_player"):
            return

        player = self.parent_window.bgm_player
        tracks = player.get_all_tracks()

        # Clear existing buttons
        self.clear_bgm_tracks()

        if not tracks:
            return

        for track in tracks:
            track_name = track.rsplit(".", 1)[0]  # Remove extension
            btn = QPushButton(track_name)
            btn.clicked.connect(lambda checked, t=track: self.select_bgm_track(t))
            self.bgm_tracks_layout.addWidget(btn)
            self.bgm_tracks_buttons[track] = btn

    def select_bgm_track(self, track_filename):
        """Load and play selected BGM track"""
        if not hasattr(self, "parent_window") or self.parent_window is None:
            QMessageBox.warning(self, "BGM", "BGM controller not available.")
            return

        player = self.parent_window.bgm_player
        if player.load_track(track_filename):
            player.play()
            self.update_bgm_status()
            QMessageBox.information(self, "BGM", f"Now playing: {track_filename}")
        else:
            QMessageBox.warning(self, "BGM", f"Failed to load: {track_filename}")

    def open_shop(self):
        if self.pet is None:
            QMessageBox.warning(self, "Shop", "Pet data not available.")
            return

        item_lines = []
        for item_name, item_data in self.shop_system.items.items():
            price = item_data.get("price", 0)
            hunger = item_data.get("hunger", 0)
            happiness = item_data.get("happiness", 0)
            item_lines.append(
                f"{item_name}: {price} coins, hunger +{hunger}, happiness +{happiness}"
            )

        item_list = "\n".join(item_lines)
        item_choice, ok = QInputDialog.getText(
            self,
            "Shop",
            f"Available items:\n{item_list}\n\nEnter item name to buy:",
        )

        if not ok or not item_choice:
            return

        item_choice = item_choice.strip().lower()
        success, message = self.shop_system.buy_item(self.pet, item_choice)

        if success:
            QMessageBox.information(self, "Shop", message)
            self.update_coin_label()
            self.refresh_inventory()
        else:
            QMessageBox.warning(self, "Shop", message)

    # =========================
    # Developer Mode Functions
    # =========================
    def toggle_developer_mode(self):
        """Toggle developer mode on/off"""
        self.developer_mode = not self.developer_mode
        self.refresh_feature_access()
        
        if self.developer_mode:
            self.dev_mode_toggle.setText("Disable Developer Mode")
            self.dev_mode_toggle.setStyleSheet(
                "QPushButton { background-color: #90EE90; color: black; }"
            )
            self.show_dev_controls()
            # Notify parent window to enter dev mode
            if hasattr(self, "parent_window") and self.parent_window is not None:
                self.parent_window.enter_developer_mode()
        else:
            self.dev_mode_toggle.setText("Enable Developer Mode")
            self.dev_mode_toggle.setStyleSheet("")
            self.hide_dev_controls()
            # Notify parent window to exit dev mode
            if hasattr(self, "parent_window") and self.parent_window is not None:
                self.parent_window.exit_developer_mode()

    def show_dev_controls(self):
        """Show developer mode controls"""
        self.states_label.show()
        self.actions_label.show()
        self.exit_dev_button.show()
        
        # Create state buttons
        states = ["happy", "hungry", "starving"]
        for state in states:
            if state not in self.state_buttons:
                btn = QPushButton(state.capitalize())
                btn.setCheckable(True)
                btn.clicked.connect(lambda checked, s=state: self.set_dev_state(s))
                self.states_layout.addWidget(btn)
                self.state_buttons[state] = btn
        
        # Create action buttons
        actions = ["idle", "petting", "jump", "roll", "sleep"]
        for action in actions:
            if action not in self.action_buttons:
                btn = QPushButton(action.capitalize())
                btn.setCheckable(True)
                btn.clicked.connect(lambda checked, a=action: self.set_dev_action(a))
                self.actions_layout.addWidget(btn)
                self.action_buttons[action] = btn

    def hide_dev_controls(self):
        """Hide developer mode controls"""
        self.states_label.hide()
        self.actions_label.hide()
        self.exit_dev_button.hide()
        
        # Reset button states
        for btn in self.state_buttons.values():
            btn.setChecked(False)
        for btn in self.action_buttons.values():
            btn.setChecked(False)

    def set_dev_state(self, state_name):
        """Set pet to a specific state for testing"""
        if not self.pet:
            return
        
        # Uncheck other state buttons
        for name, btn in self.state_buttons.items():
            if name != state_name:
                btn.setChecked(False)
        
        # Clear any action when setting state directly
        self.pet.action = None
        self.pet.action_timer = 9999  # Continuous display of state animation
        self.pet.state = state_name
        
        # Reset action buttons
        for btn in self.action_buttons.values():
            btn.setChecked(False)

        # Immediately refresh the displayed animation
        if hasattr(self, "parent_window") and self.parent_window is not None:
            self.parent_window.load_character_asset()
        
        print(f"Developer Mode: Set state to {state_name}")

    def set_dev_action(self, action_name):
        """Set pet to a specific action for testing"""
        if not self.pet:
            return
        
        # Uncheck other action buttons
        for name, btn in self.action_buttons.items():
            if name != action_name:
                btn.setChecked(False)
        
        self.pet.action = action_name
        self.pet.action_timer = 9999  # Keep the action active indefinitely in dev mode
        
        # Reset state buttons
        for btn in self.state_buttons.values():
            btn.setChecked(False)

        # Immediately refresh the displayed animation
        if hasattr(self, "parent_window") and self.parent_window is not None:
            self.parent_window.load_character_asset()
        
        print(f"Developer Mode: Set action to {action_name}")

    def exit_developer_mode(self):
        """Exit developer mode and restore normal gameplay"""
        self.dev_mode_toggle.setChecked(False)
        self.toggle_developer_mode()

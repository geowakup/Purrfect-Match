"""Compatibility wrapper for the shared daily quest demo."""

from test_daily_quests import run_quest_demo


if __name__ == "__main__":
    run_quest_demo()

        self.coins.setText(
            f"🪙 Coins: {self.rewards.get_balance()}"
        )


    def load_quests(self):

        while self.quest_layout.count():
            child = self.quest_layout.takeAt(0)

            if child.widget():
                child.widget().deleteLater()

        quests = self.quests.get_quests()

        for quest in quests:

            if quest["completed"] and not quest.get("reward_claimed", False):

                self.rewards.add_reward(
                    quest["reward"],
                    quest["name"]
                )

                QMessageBox.information(
                    self,
                    "🎉 Quest Completed!",
                    f"You earned {quest['reward']} Coins!\n\nKeep it up!"
                )

                quest["reward_claimed"] = True
                self.quests.save_quests(quests)

            card = QFrame()

            if quest["completed"]:
                card.setStyleSheet("""
                    background:#D5F5E3;
                    border:2px solid #58D68D;
                    border-radius:12px;
                    padding:15px;
                """)
            else:
                card.setStyleSheet("""
                    background:white;
                    border:2px solid #F5B7B1;
                    border-radius:12px;
                    padding:8px;
                """)

            card_layout = QVBoxLayout()
            card_layout.setSpacing(5)
            card_layout.setContentsMargins(10, 10, 10, 10)

            if quest["completed"]:
                status = QLabel("✅ COMPLETED")
                status.setStyleSheet("""
                    color:green;
                    font-weight:bold;
                    font-size:15px;
                """)
                card_layout.addWidget(status)

            title = QLabel(f"🐾 {quest['name']}")
            title.setStyleSheet("""
                font-size:16px;
                font-weight:bold;
            """)

            card_layout.addWidget(title)

            progress = QLabel(
                f"📊 Progress : {quest['progress']} / {quest['goal']}"
            )

            card_layout.addWidget(progress)

            reward = QLabel(
                f"🪙 Reward : {quest['reward']} Coins"
            )

            reward.setStyleSheet("""
                color:#D68910;
                font-weight:bold;
            """)

            card_layout.addWidget(reward)

            progress_bar = QProgressBar()
            progress_bar.setMaximum(quest["goal"])
            progress_bar.setValue(quest["progress"])
            progress_bar.setTextVisible(False)

            progress_bar.setStyleSheet("""
                QProgressBar{
                    border:2px solid #FFB69B4;
                    border-radius:8px;
                    background:#FFE4EC;                   
                    text-align:center;
                    height:18px;
                }

                QProgressBar::chunk{
                    background:#FF69B4;
                    border-radius:8px;
                }
            """)

            card_layout.addWidget(progress_bar)

            card.setLayout(card_layout)

            self.quest_layout.addWidget(card)

        self.load_pet()


    def feed_pet(self):

        if self.rewards.spend_reward(10, "Feed Pet"):

            self.pet.give_reward(food=10, happiness=5)

            self.load_pet()

            self.status.setText("😸 Yum! Your pet loved the food!")

        else:

            self.status.setText("❌ Not enough coins!")


if __name__ == "__main__":

    import sys

    app = QApplication(sys.argv)

    window = DailyQuestApp()
    window.show()

    sys.exit(app.exec())   
    def update_header(self):
        self.stats_label.config(
            text=f"🍖 Hunger: {self.hunger}\n😊 Happiness: {self.happiness}"
        )
        self.coins_label.config(
            text=f"Coins: {self.rewards.get_balance()}"
        )

    def load_quests(self):
        for widget in self.quest_list_frame.winfo_children():
            widget.destroy()

        quest_data = self.quest_system.get_quests()

        if not quest_data:
            empty_label = tk.Label(
                self.quest_list_frame,
                text="No quests available.",
                font=("Segoe UI", 12),
                bg="#FFF0F5",
                fg="#8B3A62",
                pady=10
            )
            empty_label.pack(pady=10)
            return

        for quest in quest_data:
            completed_text = " ✅" if quest.get("completed", False) else ""
            quest_text = f"{quest['progress']}/{quest['goal']} - {quest.get('name', quest.get('title', 'Unknown'))}{completed_text}"
            quest_label = tk.Label(
                self.quest_list_frame,
                text=quest_text,
                font=("Segoe UI", 12),
                bg="#FFF0F5",
                fg="#8B3A62",
                anchor="w",
                justify="left",
                padx=10,
                pady=8
            )
            quest_label.pack(fill="x", padx=10, pady=4)

        self.update_header()

    def feed_pet(self):
        if self.rewards.get_balance() < 10:
            self.status_label.config(text="🐱 Not enough coins!")
            return

        self.rewards.spend_reward(10, "Fed pet")
        self.quest_system.update_progress("Complete 1 task")

        self.hunger = min(self.hunger + 10, 100)
        self.happiness = min(self.happiness + 5, 100)

        self.update_header()
        self.load_quests()
        self.status_label.config(text="🐱 Yum! Your pet is happy!")

    def decay(self):
        self.hunger = max(self.hunger - 1, 0)
        self.happiness = max(self.happiness - 1, 0)
        self.update_header()
        self.window.after(5000, self.decay)


if __name__ == "__main__":
    PurrfectMatchApp()

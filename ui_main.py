from system.reward_manager import RewardSystem
from system.quest_system import QuestSystem
import tkinter as tk

# MAIN WINDOW
window = tk.Tk()
quests = QuestSystem()
quests.update_progress("Open app 3 times")
quest_data = quests.get_quests()
rewards = RewardSystem()
hunger = 100
happiness = 100
rewards.add_reward(20, "Starting coins")

window.title("Purrfect Match 🐾")
window.geometry("500x650")
window.configure(bg="#FFE4EC")  # pastel pink background

# TITLE
title = tk.Label(
    window,
    text="🐾Purrfect Match 🐾",
    font=("Comic Sans MS", 22, "bold"),
    bg="#FFE4EC",
    fg="#FF4F87"
)
title.pack(pady=15)

# PET DISPLAY
pet_label = tk.Label(
    window,
    text="🐱",
    font=("Arial", 70),
    bg="#FFE4EC"
)
pet_label.pack()
stats = tk.Label(
    window,
    text="🍖 Hunger: 100\n😊 Happiness: 100",
    font=("Comic Sans MS", 12),
    bg="#FFF0F5",
    fg="#8B3A62",
    padx=15,
    pady=10
)

stats.pack(pady=10)

# COINS DISPLAY
coins = tk.Label(
    window,
    text=" Coins: 20",
    font=("Comic Sans MS", 14, "bold"),
    bg="#FFF0F5",
    fg="#C71585",
    padx=15,
    pady=10
)
coins.pack(pady=10)

# QUEST TITLE
quest_title = tk.Label(
    window,
    text=" Daily Quests ",
    font=("Comic Sans MS", 16, "bold"),
    bg="#FFE4EC",
    fg="#DB3E6F"
)
quest_title.pack(pady=10)

def load_quests():

    quest_data = quests.get_quests()

    for quest in quest_data:

        quest_text = f"{quest['progress']}/{quest['goal']} - {quest['name']}"

        quest_label = tk.Label(
            window,
            text=quest_text,
            font=("Segoe UI", 12),
            bg="#FFF0F5",
            width=30,
            pady=8
        )

        quest_label.pack(pady=5)


load_quests()

def feed_pet():

    global hunger, happiness

    if rewards.get_balance() >= 10:

        rewards.spend_reward(10, "Fed pet")
        quests.update_progress("Complete 1 task")

        coins.config(
            text=f" Coins: {rewards.get_balance()}"
        )
        
        hunger = min(hunger + 10, 100)
        happiness = min(happiness + 5, 100)

        stats.config(
            text=f" Hunger:  {hunger}\n Happiness: {happiness}"
        )


        status.config(
            text="🐱 Yum! Your pet is happy!"
        )

    else:

        status.config(
            text="😿 Not enough coins!" 
        )
# FEED BUTTON
feed_button = tk.Button(
    window,
        text="🍖 Feed Pet",
    command=feed_pet,
    font=("Comic Sans MS", 13, "bold"),
    bg="#FF69B4",
    fg="white",
    padx=15,
    pady=8,
    relief="raised",
    bd=4
)
feed_button.pack(pady=25)

# STATUS MESSAGE
status = tk.Label(
    window,
    text="🐱 Pet is waiting for food!",
    font=("Segoe UI", 11),
    bg="#FFE4EC",
    fg="#8B3A62",
)
status.pack()

def decay():

    global hunger, happiness

    hunger = max(hunger - 1, 0)
    happiness = max(happiness - 1, 0)

    stats.config(
        text=f"🍖 Hunger: {hunger}\n😊 Happiness: {happiness}"
    )

    window.after(5000, decay)


decay()

# RUN WINDOW
window.mainloop()
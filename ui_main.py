import tkinter as tk

# MAIN WINDOW
window = tk.Tk()
window.title("Purrfect Match 🐾")
window.geometry("500x500")
window.configure(bg="#FFE4EC")  # pastel pink background

# TITLE
title = tk.Label(
    window,
    text="🐾 Purrfect Match 🐾",
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

# COINS DISPLAY
coins = tk.Label(
    window,
    text="💰 Coins: 20",
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
    text="🌟 Daily Quests 🌟",
    font=("Comic Sans MS", 16, "bold"),
    bg="#FFE4EC",
    fg="#DB3E6F"
)
quest_title.pack(pady=10)

# QUESTS
quest1 = tk.Label(
    window,
    text="✅ Complete 1 task",
    font=("Segoe UI", 12),
    bg="#FFF0F5",
    width=30,
    pady=8
)
quest1.pack(pady=5)

quest2 = tk.Label(
    window,
    text="✅ Open app 3 times",
    font=("Segoe UI", 12),
    bg="#FFF0F5",
    width=30,
    pady=8
)
quest2.pack(pady=5)

# FEED BUTTON
feed_button = tk.Button(
    window,
    text="🍖 Feed Pet",
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
    text="✨ Your pet is happy today!",
    font=("Segoe UI", 11),
    bg="#FFE4EC",
    fg="#8B3A62"
)
status.pack()

# RUN WINDOW
window.mainloop()
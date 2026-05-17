# =========================
# timer_loop.py
# =========================

import random

from PySide6.QtCore import QTimer


class TimerLoop:

    def __init__(self, pet, callback=None, interval=200):

        self.pet = pet

        # Optional GUI callback
        self.callback = callback

        # Qt timer
        self.timer = QTimer()

        # Run update_loop repeatedly
        self.timer.timeout.connect(self.update_loop)

        # milliseconds
        self.interval = interval

    # =========================
    # START LOOP
    # =========================
    def start(self):

        print("Starting pet simulation...\n")

        self.timer.start(self.interval)

    # =========================
    # UPDATE LOOP
    # =========================
    def update_loop(self):

        # -------------------------
        # RANDOM ACTION SYSTEM
        # -------------------------
        if random.randint(1, 25) == 1:
            self.pet.trigger_random_action()

        # -------------------------
        # DISPLAY STATUS
        # -------------------------
        print("\n====================")
        print(self.pet.status())

        # -------------------------
        # GUI CALLBACK
        # -------------------------
        if self.callback:
            self.callback()

    # =========================
    # STOP LOOP
    # =========================
    def stop(self):

        self.timer.stop()

        print("Timer stopped.")
# =========================
# timer_loop.py
# =========================

import time
import random


class TimerLoop:

    def __init__(self, pet, tick_rate=1.0):

        self.pet = pet
        self.tick_rate = tick_rate
        self.running = False

    # =========================
    # MAIN LOOP
    # =========================
    def start(self):

        self.running = True

        print("Starting pet simulation...\n")

        while self.running:

            start_time = time.time()

            # -------------------------
            # RANDOM ACTION SYSTEM
            # -------------------------
            if random.randint(1, 5) == 1:
                self.pet.trigger_random_action()

            # -------------------------
            # UPDATE PET
            # -------------------------
            self.pet.update()

            # -------------------------
            # DISPLAY STATUS
            # -------------------------
            print("\n====================")
            print(self.pet.status())

            # -------------------------
            # TICK CONTROL
            # -------------------------
            elapsed = time.time() - start_time
            sleep_time = self.tick_rate - elapsed

            if sleep_time > 0:
                time.sleep(sleep_time)

    # =========================
    # STOP LOOP
    # =========================
    def stop(self):

        self.running = False
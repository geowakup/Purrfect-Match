class DogCharacter:

    def __init__(self):
        self.states = {
            "happy": [
                "dog-happy-1.png",
                "dog-happy-2.png",
                "dog-happy-3.png",
                "dog-happy-4.png"
            ],
            "hungry": [
                "dog-hungry-1.png",
                "dog-hungry-2.png",
                "dog-hungry-3.png",
                "dog-hungry-4.png"
            ],
            "starving": [
                "dog-starving-1.png",
                "dog-starving-2.png",
                "dog-starving-3.png",
                "dog-starving-4.png"
            ],
            "petting": [
                "dog-petting-1.png",
                "dog-petting-2.png",
                "dog-petting-3.png",
                "dog-petting-4.png"
            ],
            "jump": [
                "dog-jump-1.png",
                "dog-jump-2.png",
                "dog-jump-3.png",
                "dog-jump-4.png"
            ],
            "roll": [
                "dog-roll-1.png",
                "dog-roll-2.png",
                "dog-roll-3.png",
                "dog-roll-4.png"
            ],
            "sleep": [
                "dog-sleep-1.png",
                "dog-sleep-2.png",
                "dog-sleep-3.png",
                "dog-sleep-4.png"
            ],
            "idle": [
                "dog-idle-1.png",
                "dog-idle-2.png",
                "dog-idle-3.png",
                "dog-idle-4.png"
            ],
        }

    def get_file(self, state):
        return self.states.get(state, [
            "dog-idle-1.png",
            "dog-idle-2.png",
            "dog-idle-3.png",
            "dog-idle-4.png"
        ])

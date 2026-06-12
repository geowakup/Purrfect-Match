class FireflyCharacter:

    def __init__(self):
        self.states = {
            "happy": [
                "firefly-happy-1.png",
                "firefly-happy-2.png",
                "firefly-happy-3.png",
                "firefly-happy-4.png"
            ],
            "hungry": [
                "firefly-hungry-1.png",
                "firefly-hungry-2.png",
                "firefly-hungry-3.png",
                "firefly-hungry-4.png"
            ],
            "starving": [
                "firefly-starving-1.png",
                "firefly-starving-2.png",
                "firefly-starving-3.png",
                "firefly-starving-4.png"
            ],
            "petting": [
                "firefly-petting-1.png",
                "firefly-petting-2.png",
                "firefly-petting-3.png",
                "firefly-petting-4.png"
            ],
            "jump": [
                "firefly-jump-1.png",
                "firefly-jump-2.png",
                "firefly-jump-3.png",
                "firefly-jump-4.png"
            ],
            "roll": [
                "firefly-roll-1.png",
                "firefly-roll-2.png",
                "firefly-roll-3.png",
                "firefly-roll-4.png"
            ],
            "sleep": [
                "firefly-sleep-1.png",
                "firefly-sleep-2.png",
                "firefly-sleep-3.png",
                "firefly-sleep-4.png"
            ],
        }

    def get_file(self, state):
        return self.states.get(state, [
            "firefly-idle-1.png",
            "firefly-idle-2.png",
            "firefly-idle-3.png",
            "firefly-idle-4.png"
        ])
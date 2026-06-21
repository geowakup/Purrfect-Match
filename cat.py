class CatCharacter:

    def __init__(self):
        self.states = {
            "happy": [
                "cat-happy-1.png",
                "cat-happy-2.png",
                "cat-happy-3.png",
                "cat-happy-4.png"
            ],
            "hungry": [
                "cat-hungry-1.png",
                "cat-hungry-2.png",
                "cat-hungry-3.png",
                "cat-hungry-4.png"
            ],
            "starving": [
                "cat-starving-1.png",
                "cat-starving-2.png",
                "cat-starving-3.png",
                "cat-starving-4.png"
            ],
            "petting": [
                "cat-petting-1.png",
                "cat-petting-2.png",
                "cat-petting-3.png",
                "cat-petting-4.png"
            ],
            "jump": [
                "cat-jump-1.png",
                "cat-jump-2.png",
                "cat-jump-3.png",
                "cat-jump-4.png"
            ],
            "roll": [
                "cat-roll-1.png",
                "cat-roll-2.png",
                "cat-roll-3.png",
                "cat-roll-4.png"
            ],
            "sleep": [
                "cat-sleep-1.png",
                "cat-sleep-2.png",
                "cat-sleep-3.png",
                "cat-sleep-4.png"
            ],
        }

    def get_file(self, state):
        return self.states.get(state, [
            "cat-happy-1.png",
            "cat-happy-2.png",
            "cat-happy-3.png",
            "cat-happy-4.png"
        ])
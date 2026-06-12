class CatCharacter:

    def __init__(self):
        self.states = {
            "happy": "cat-happy.jpg",
            "hungry": "cat-eating.jpg",
            "starving": "cat-eating.jpg",
            "petting": "cat-petting.jpg",
            "jump": "cat-jumpping.jpg",
            "roll": "cat-rolling.jpg",
            "sleep": "cat-sleeping.jpg",
        }

    def get_file(self, state):
        return self.states.get(state, "cat-idle.jpg")
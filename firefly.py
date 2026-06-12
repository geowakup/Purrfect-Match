class FireflyCharacter:

    def __init__(self):
        self.states = {
            "happy": "firefly_idle.gif",
            "hungry": "firefly_hungry.gif",
            "starving": "firefly_starving.gif",
            "petting": "firefly_petting.gif",
            "jump": "firefly_jump.gif",
            "roll": "firefly_roll.gif",
            "sleep": "firefly_sleep.gif",
        }

    def get_file(self, state):
        return self.states.get(state, "firefly_idle.gif")
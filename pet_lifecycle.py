import random


class PetLifecycle:

    def __init__(self, pet):

        self.pet = pet

    # =========================
    # SPAWN
    # =========================
    def spawn(self):

        print("Pet spawned!")

        self.pet.hunger = 100
        self.pet.happiness = 100
        self.pet.energy = 100
        self.pet.cleanliness = 100

        self.pet.alive = True
        self.pet.age = 0

        self.pet.state = "spawn"

        self.pet.action = None
        self.pet.action_timer = 5

    # =========================
    # IDLE BEHAVIOR
    # =========================
    def idle_behavior(self):

        if not self.pet.alive:
            return

        if self.pet.action is None:

            chance = random.randint(1, 50)

            if chance == 1:
                self.pet.trigger_random_action()

    # =========================
    # DEATH CHECK
    # =========================
    def check_death(self):

        if (
            self.pet.hunger <= 0
            and self.pet.energy <= 0
        ):

            self.pet.alive = False
            self.pet.state = "dead"

            return True

        return False

    # =========================
    # RESET / REVIVE
    # =========================
    def reset(self):

        self.spawn()

        print("Pet reset!")
    
# =========================
# TEST
# =========================
if __name__ == "__main__":

    from pet import Pet

    pet = Pet()

    lifecycle = PetLifecycle(pet)

    lifecycle.spawn()

    print("Lifecycle working!")
    print(pet.status())

    lifecycle.idle_behavior()

    print("Idle behavior executed")
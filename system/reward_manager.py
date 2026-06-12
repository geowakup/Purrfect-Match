class RewardSystem:
    def __init__(self):
        self.coins = 0

    def add_reward(self, amount: int, reason: str = "") -> None:
        """Add coins as a reward."""
        self.coins += amount

        if reason:
            print(f"Reward: +{amount} coins ({reason})")
        else:
            print(f"Reward: +{amount} coins")

    def spend_reward(self, amount, reason=""):
        if self.coins >= amount:
            self.coins -= amount
            print(f"-{amount} coins ({reason})")
        else:
            print("Not enough coins.")

    def get_balance(self):
        return self.coins
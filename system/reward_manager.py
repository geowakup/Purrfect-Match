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

    def spend_coins(self, amount: int) -> bool:
        """Spend coins if enough balance exists."""
        if amount <= self.coins:
            self.coins -= amount
            return True
        return False

    def get_balance(self) -> int:
        """Return current coin balance."""
        return self.coins

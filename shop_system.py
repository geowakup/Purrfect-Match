# =========================
# shop_system.py
# =========================

class ShopSystem:

    def __init__(self):

        self.items = {

            "apple": {
                "price": 10,
                "hunger": 15,
                "happiness": 0
            },

            "fish": {
                "price": 20,
                "hunger": 30,
                "happiness": 5
            },

            "cake": {
                "price": 50,
                "hunger": 10,
                "happiness": 25
            },

            "ball": {
                "price": 30,
                "happiness": 20
            }
        }

    # =========================
    # BUY ITEM
    # =========================
    def buy_item(self, pet, item_name):

        if item_name not in self.items:
            return False, "Item does not exist."

        item = self.items[item_name]

        if pet.coins < item["price"]:
            return False, "Not enough coins."

        pet.coins -= item["price"]
        pet.inventory.append(item_name)

        if getattr(pet, "save_callback", None) is not None:
            try:
                pet.save_callback()
            except Exception as exc:
                print(f"Failed to save after purchase: {exc}")

        return True, f"Bought {item_name} for {item['price']} coins!"

    # =========================
    # USE ITEM
    # =========================
    def use_item(self, pet, item_name):

        # Item not owned
        if item_name not in pet.inventory:

            return False, "Item not in inventory"

        item = self.items[item_name]

        # Apply effects
        pet.hunger = min(
            100,
            pet.hunger + item.get("hunger", 0)
        )

        pet.happiness = min(
            100,
            pet.happiness + item.get("happiness", 0)
        )

        # Remove used item
        pet.inventory.remove(item_name)

        if getattr(pet, "save_callback", None) is not None:
            try:
                pet.save_callback()
            except Exception as exc:
                print(f"Failed to save after use: {exc}")

        return True, f"Used {item_name}!"
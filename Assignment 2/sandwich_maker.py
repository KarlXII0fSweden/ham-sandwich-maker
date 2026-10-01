class SandwichMaker:
    def __init__(self, resources):
        self.machine_resources = resources

    def check_resources(self, ingredients):
        """Return whether the machine has enough of each ingredient."""
        for ingredient, amount_needed in ingredients.items():
            if self.machine_resources.get(ingredient, 0) < amount_needed:
                print(f"Sorry, there is not enough {ingredient}.")
                return False
        return True

    def make_sandwich(self, sandwich_size, order_ingredients):
        """Deduct ingredients for a paid order and announce completion."""
        for ingredient, amount_needed in order_ingredients.items():
            self.machine_resources[ingredient] -= amount_needed
        print(f"Here is your {sandwich_size} sandwich. Enjoy!")

class Cashier:
    def __init__(self):
        pass

    def process_coins(self):
        """Ask for coin counts and return the total in dollars."""
        print("Please insert coins.")
        quarters = int(input("How many quarters?: "))
        dimes = int(input("How many dimes?: "))
        nickels = int(input("How many nickels?: "))
        pennies = int(input("How many pennies?: "))
        return quarters * 0.25 + dimes * 0.10 + nickels * 0.05 + pennies * 0.01

    def transaction_result(self, coins, cost):
        """Accept sufficient payment and return change; otherwise refund."""
        if coins < cost:
            print("Sorry, that's not enough money. Money refunded.")
            return False
        print(f"Here is ${coins - cost:.2f} in change.")
        return True

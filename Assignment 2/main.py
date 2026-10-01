import data
from sandwich_maker import SandwichMaker
from cashier import Cashier


resources = data.resources
recipes = data.recipes
sandwich_maker_instance = SandwichMaker(resources)
cashier_instance = Cashier()


def main():
    while True:
        choice = input("What would you like? (small/medium/large): ").strip().lower()
        if choice == "off":
            break
        if choice == "report":
            for ingredient, amount in resources.items():
                print(f"{ingredient}: {amount}")
            continue
        if choice not in recipes:
            print("Please choose small, medium, large, report, or off.")
            continue

        recipe = recipes[choice]
        ingredients = recipe["ingredients"]
        if not sandwich_maker_instance.check_resources(ingredients):
            continue
        payment = cashier_instance.process_coins()
        if cashier_instance.transaction_result(payment, recipe["cost"]):
            sandwich_maker_instance.make_sandwich(choice, ingredients)


if __name__ == "__main__":
    main()

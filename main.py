# Import necessary Libraries
import errno
from data import MENU, resources, Money


def report(storage):
    """Brief report about the sources in the machine"""
    print("The following resources are available:")
    for key in storage:
        if key == "money":
            print(f"{key.title()}: {storage[key]}$")
        else:
            print(f"{key.title()}: {storage[key]}ml")


def enough_ingredients(choice, storage, menu):
    """Check if we have enough ingredient for the user drink"""
    ingredients = menu[choice]["ingredients"]
    for key in ingredients:
        if storage[key] <= ingredients[key]:
            print(f"The machine does not have enough {key}. We are sorry for that. ")
            return False
        else:
            continue
    return True


def take_money(currencies):
    """Calculate the inserted amount of miney to the machine"""
    print("Insert your coins to the machine")
    balance = 0.0

    for key in currencies:
        count = int(input(f"How many {key} do you want to insert?"))
        while count == errno:
            count = int(input(f"You did not insert a valid number.\nHow many {key} do you want to insert?"))
        balance += count * currencies[key]

    return balance


def enough_money(choice, balance, menu):
    """Check whether the inserted money is enough to pay the drink cost or not"""
    if balance >= menu[choice]["cost"]:
        print("Please, waite...")
        return True
    else:
        print("You did not insert enough money!\nYou can take back Your money.\nHave a good day")
        return False


def make_coffe(choice, balance, storage, menu):
    """Subtract the necessary resources from the storage and calculate the rest to be paid back"""
    ingredients = menu[choice]["ingredients"]

    # Subtracting the necessary resources from storage
    for key in ingredients:
        storage[key] -= ingredients[key]

    # Add the drink cost to the storage
    storage["money"] = storage["money"] + menu[choice]["cost"]

    # Calculating the rest
    rest = balance - menu[choice]["cost"]

    # Preparing the Drink
    print('''
           ########
          #        #
          #        #
          #        #
          #        #
          ##########
          ''')
    print("Enjoy your coffe!")

    # rest alert
    if rest != 0.0:
        print(f"Do not for get to take the {rest}$.")
    return storage


def main(menu, storage, currencies):
    # Take the User choice of drink
    answer = input("What would you like to have? (espresso/latte/cappuccino)").lower()

    # Check whether the user input is valid or not and if not repeat to get a valid answer
    while answer not in menu.keys() and answer != "report" and answer != "off":
        print("You did not insert a valid choice. Please select from the available options.")
        answer = input("What would you like to have? (espresso/latte/cappuccino)")

    # If the User asks for the Report.
    if answer == "report":
        report(storage=storage)
        return True, storage

    # If User wants the machine to turn off.
    elif answer == "off":
        print("Goodbye!")
        return False, storage

    # If User wants to order a drink.
    else:

        # If there i enough ingredients
        if enough_ingredients(choice=answer, storage=storage, menu=menu):

            # calculate the balance inserted to the machine
            user_balance = take_money(currencies=currencies)

            # Check if the balance is enough to get the drink
            if enough_money(choice=answer, balance=user_balance, menu=menu):

                # Updating the Storage
                storage_updated = make_coffe(choice=answer, balance=user_balance, storage=storage, menu=menu)
                return True, storage_updated

            else:
                return True, storage
        else:
            return True, storage


machine_statuses, new_storage = main(menu=MENU,storage=resources,currencies=Money)
while machine_statuses:
    machine_statuses, new_storage = main(menu=MENU, storage=new_storage, currencies=Money)








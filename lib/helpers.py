from models.user import User
from models.plant import Plant
from models.action import Action
from seed import start_program
from rich.console import Console

console = Console()
EXIT_WORDS = ["6", "exit", "quit"]


def welcome():
    console.rule("[bold green]Plant Provider: Dead or Alive :seedling:")
    start_program()


def menu():
    console.print("Please select an option: ", style="bold underline green on white")
    console.print("1. Start Plant Provider: Dead or Alive")
    console.print("2. View the rules")
    console.print("3. View scoreboard")
    console.print("4. Find User")
    console.print("5. Find Users")
    console.print("6. Exit the program")


def exit_program():
    console.print("Thanks for playing! Come back soon!", style="bold")
    exit()


def find_or_create_user():  # sourcery skip: extract-method

    name = input("Enter your username: ").strip()

    if name.lower() in EXIT_WORDS:
        exit_program()

    user = User.find_by_name(name)

    if user is None:
        new_user = User.create(name)
        console.print(f"Welcome {new_user.name}!")
        plant_name = input("Enter your plant's name: ").strip()

        if plant_name.lower() in EXIT_WORDS:
            exit_program()

        new_plant = Plant.create(plant_name)
        new_association = Action.create("Water", new_user.id, new_plant.id)
        console.print(f"Thank you for purchasing your new plant {new_plant.name}!")

    else:
        console.print(f"Welcome back {user.name}! Your plant is waiting for you!", style="bold")
        #retrieve plants information
        start_game(user)


def start_game(user):
    # console.print("Welcome to Plant Provider: Dead or Alive!")
    console.print("Please select one of the options below: ")
    console.print("1. Take care of your plant")
    console.print("2. View your plants")
    console.print("3. Delete User")
    console.print("4. Exit out of program")

    user_input = input("> ").strip().lower()
    
    if user_input in EXIT_WORDS:
        exit_program()

    if user_input == "1":
        check_condition(user)
    elif user_input == "2":
        view_inventory()
    elif user_input == "3":
        delete_user()
    elif user_input == "4":
        exit_program()


def check_condition(user):
    console.print("Your plant is in need of something! What does it need?")
    console.print("1. Does it need moisture? Type: [underline]Water[/]")
    console.print("2. Does it need sunlight? Type: [underline]Sunlight[/]")
    console.print("3. Your plant might be satisfied as is! Type: [underline]Nothing[/]!")
    console.print("4. Would you like to check your plant's status? Type: [underline]Check status[/]")
    selected_condition = input("What does your plant need?: ").strip().lower()

    if selected_condition in EXIT_WORDS:
        exit_program()

    if selected_condition not in [
        "water",
        "sunlight",
        "nothing",
        "check status"
    ]:
        console.print("Please pick one of the provided options!")
        return check_condition(user)

    if selected_condition is "check status":
        return user.plant()
    if selected_condition in [
        "water",
        "sunlight",
        "nothing",
        # "plant status"
    ]:
        user.update_user_action() #invoke correctly
        user.compare_condition()
        console.print("You selected one of the options")


def view_rules():
    welcome()
    console.print("Your goal is to grow your plant to the fullest.")
    console.print("Here are the basic instructions:")
    console.print("1. Your plant will decide on what it is required to grow.")
    console.print(
        "2. You must guess the correct demand that the plant wants in 5 days."
    )
    console.print("3. If you do not guess within the given days, your plant will die.")
    console.print(
        "4. Your plant information will be stored and you can always go back and lurk your failed attempts."
    )


def view_scoreboard():
    pass


def delete_user():
    username = input("Confirm your username: ").strip()

    if username.lower() in EXIT_WORDS:
        exit_program()

    if user := User.find_by_name(username):
        user.delete()
        console.print(f"Successfully deleted {username}")


def find_user():
    name = input("Enter your username: ").strip()

    if name.lower() in EXIT_WORDS:
        exit_program()

    if user := User.find_by_name(name):
        (
            console.print(f"You already created an username {name} with us!")
            if user
            else print("No username exists")
        )
    else:
        console.print("No user exist in our database")


def find_users():

    if users := User.get_all():
        for user in users:
            print(user)
    else:
        console.print("There are no users playing this game :(")

def view_inventory():
    pass
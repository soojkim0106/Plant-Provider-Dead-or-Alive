from models.user import User
from models.plant import Plant
from models.action import Action
from seed import start_program
from rich.console import Console

console = Console()
EXIT_WORDS = ["7", "exit", "quit"]


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
    console.print("6. Delete User")
    console.print("7. Exit the program")


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
        new_action = Action.create("Water", new_user.id, new_plant.id)
        console.print(f"Thank you for purchasing your new plant {new_plant.name}!")
        start_game(new_action)
    else:
        console.print(f"Welcome back {user.name}! Your plant is waiting for you!")
        #retrieve plants information
        start_game(user)


def start_game(user):
    check_condition(user)


def check_condition(user):
    console.print("Your plant is in need of something! What does it need?")
    console.print("1. Does it need moisture? Type: [underline]Water[/]")
    console.print("2. Does it need sunlight? Type: [underline]Sunlight[/]")
    console.print("3. Your plant might be satisfied as is! Type: [underline]Nothing[/]!")
    console.print("4. Would you like to check your plant's status? Type: [underline]Check status[/]")
    selected_condition = input("What does your plant need?: ").strip().lower()

    if selected_condition == EXIT_WORDS:
        exit_program()

    if selected_condition not in [
        "water",
        "sunlight",
        "nothing",
        # "plant status"
    ]:
        console.print("Please pick one of the provided options!")
        return check_condition(user)

    if selected_condition in [
        "water",
        "sunlight",
        "nothing",
        # "plant status"
    ]:
        Action.update_user_action(user, selected_condition) #invoke correctly
        Action.compare_condition(user)
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
    username = input("Enter your username: ").strip()

    if username.lower() in EXIT_WORDS:
        exit_program()

    if user := User.find_by_name(username):
        user.delete()
        console.print(f"Successfully deleted {username}")
    else:
        console.print(f"We could not locate {username}. Failed to delete.")


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

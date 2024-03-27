from models.user import User
from models.plant import Plant
from models.action import Action
from seed import start_program
from rich.console import Console
import click
import ipdb

console = Console()
EXIT_WORDS = ["exit", "quit", "c"]


def welcome():
    click.clear()
    console.rule("[bold green]Plant Provider: Dead or Alive :seedling:")
    start_program()


def menu():
    console.print(
        """
                    _
                  _(_)_                          wWWWw   _
      @@@@       (_)@(_)   vVVVv     _     @@@@  (___) _(_)_
     @@()@@ wWWWw  (_)\    (___)   _(_)_  @@()@@   Y  (_)@(_)
      @@@@  (___)     `|/    Y    (_)@(_)  @@@@   \|/   (_)|
       /      Y       \|    \|/    /(_)    \|      |/      |
    \ |     \ |/       | / \ | /  \|/       |/    \|      \|/
    |||//   |||///  ||\|//""\|/// \|///  ||\|//  |||//  ||\|// 
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        """,
        style="yellow",
    )
    console.print("Please select an option: ", style="bold underline green on white")
    console.print("1. Start Plant Provider: Dead or Alive")
    console.print("2. View the rules")
    console.print("3. Exit the program")


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
        [picked_plant, picked_plant_id] = pick_plant()
        new_association = Action.create("Water", new_user.id, picked_plant_id)
        console.print(f"Thank you for purchasing your new plant {picked_plant.name}!")
        start_game(new_user, new_association, picked_plant)  
        return new_user
    else:
        [picked_plant, picked_plant_id] = pick_plant()
        #
        console.print(
            f"Welcome back {user.name}! Your plant {picked_plant.name} waiting for you!",
            style="bold",
        )
        new_association = Action.create("Purchase", user.id, picked_plant_id)
        # retrieve plants information
        start_game(user, new_association, picked_plant)
        return user


def start_game(user, new_association, picked_plant):
    while True:
        # click.clear()
        console.print(
            """
                ⣿⣿⣿⣿⣿⣿⣿⣿⡿⠿⠿⢿⣿⣿⣿⣿⢉⣩⠉⣛⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                ⣿⣿⣿⣿⡿⠟⢋⣥⢶⣞⡷⣦⡙⠋⣡⣤⣌⠙⢧⣤⡖⠀⠙⣿⣿⣿⣿⣿⣿⡿⠿⠿⣿⣿⣿⣿⡿⠿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                ⣿⣿⣿⣿⣤⣈⡛⠋⠿⠾⠽⠓⠃⠸⠛⢳⣯⡷⣄⢙⣧⣤⢤⠘⣿⣿⣿⣿⠏⣰⣿⣦⠘⠿⠿⠋⣴⣷⣦⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                ⣿⣿⣿⣿⢿⣿⠉⣉⣄⡘⢿⡆⠄⢠⠀⣼⠁⠘⣾⠏⠻⣦⠀⠤⣿⠿⠿⠏⣸⣿⣿⣿⣇⡄⣄⣼⣿⣿⣿⡧⠹⠿⢿⣿⣿⣿⣿⣿⣿⣿
                ⣿⡿⠋⠁⢢⣤⣤⠿⠋⠁⣘⡃⠐⠘⠀⢈⣸⠄⠿⠐⡆⢿⡻⢀⣿⠶⠂⡀⣼⣟⢁⣹⡟⠈⣻⣏⢈⣿⣧⠀⢂⠘⠿⣿⣿⣿⣿⣿⣿⣿
                ⡿⢛⣉⣩⣴⠯⠋⣠⣾⢿⣻⢽⣷⠀⠀⣉⣉⡙⠲⣶⣷⣦⣤⣾⣿⡟⣰⣿⣿⡿⠿⠿⠿⠿⢿⣿⣿⣿⣿⣿⣿⣧⠸⣿⣿⣿⣿⣿⣿⣿
                ⢁⣈⡉⢳⣯⣷⢾⡻⠽⢏⡇⢀⠙⠀⠀⡿⣯⢿⣳⠘⣿⣿⣿⣿⡿⠁⠏⣩⣤⣶⣶⣷⡄⢀⠂⣈⠙⢿⣿⣿⣿⡏⠀⢹⣿⣿⣿⣿⣿⣿
                ⡋⣤⣶⡏⢠⠘⣿⠇⢠⠸⡷⠈⡆⠀⠀⡙⠫⢿⡽⠀⣿⣿⣿⢋⡴⠀⠀⢹⣿⣿⣿⣿⣿⡈⠁⠀⣴⣾⣿⣿⣿⣿⣦⠄⢻⣿⣿⣿⣿⣿
                ⣇⡙⠚⢁⣾⣀⠛⣃⣸⣤⣴⣿⣿⠀⠀⣿⣷⣶⣶⣾⣿⣿⣧⡈⢠⣑⠢⠸⣿⣿⣿⣿⡿⠿⢀⣾⣿⣿⣿⣿⣿⣿⣇⠀⠘⣿⣿⣿⣿⣿
                ⣿⣿⣿⣿⣿⣿⣿⡇⢰⣶⣶⣶⣶⣶⣶⣶⣶⣶⣶⠄⣿⣿⣿⡇⣸⣿⣿⣄⣛⣉⣩⣤⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⡆⢿⣿⣿⣿⣿
                ⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠆⣿⣿⣿⡇⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⢸⣿⣿⣿⣿
                ⣿⣿⣿⣿⣿⣿⣿⣷⣬⠉⣉⣉⣉⣉⣉⣉⣉⣉⠉⣤⣿⣿⣿⡇⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡧⢸⣿⠋⠀⠙
                ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⣿⣿⣿⣿⣿⣿⣿⡟⢸⣿⣿⣿⣿⣷⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠇⠛⠁⠺⠖⣰
                ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡇⢸⣿⣿⣿⣿⣿⣿⠇⣾⣿⣿⣿⣿⡟⢡⣌⢙⣿⣿⣿⣿⣿⣿⣿⠟⣙⠛⢿⣿⣿⣿⣿⣿⡟⠀⠸⠃⣀⣴⣿
                ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣬⣭⣭⣩⣍⣭⣭⣤⣿⣿⣿⣿⣿⣿⣦⣬⣭⣭⣭⣭⣭⣙⣉⣋⣀⣉⣉⣋⣩⣭⣭⣭⣥⣤⣶⣾⣿⣿⣿⣿
            """,
            style="green",
        )
        console.print(
            "Please select one of the options below: ",
            style="bold underline green on white",
        )
        console.print(f"1. Take care of the [underline]{picked_plant.name}")
        console.print("2. View your plants")
        console.print("3. Delete User")
        console.print("4. Plant died or is a flower? Select or purchase another!")
        console.print("5. Switch user")
        console.print("6. Exit out of program")

        user_input = input("> ").strip().lower()

        if user_input in EXIT_WORDS:
            exit_program()

        if user_input == "1":
            check_condition(user, new_association, picked_plant)  
        elif user_input == "2":
            view_inventory(user)
        elif user_input == "3":
            delete_user()
        elif user_input == "4":
            [re_picked_plant, re_picked_plant_id] = pick_plant()
            new_association = Action.create("Purchase", user.id, re_picked_plant_id)
            check_condition(user, new_association, re_picked_plant)    
        elif user_input == "5":
            user = find_or_create_user()
        elif user_input == "6":
            exit_program()

def pick_plant():
    # click.clear()
    user_input = input("What's the name of plant you are looking for? ").strip().lower()
    if user_input in EXIT_WORDS:
        exit_program()
    if Plant.find_by_name(user_input):
        console.print(f"It's time to grow {user_input} ", style="bold")
        return [Plant.find_by_name(user_input), Plant.find_by_name(user_input).id]
    else:
        _ = Plant.create(user_input)
        console.print("The plant name you mentioned does not exist")
        console.print(
            f"As your plant did not already exist, you purchased {user_input}",
            style="bold",
        )
        return [Plant.find_by_name(user_input), Plant.find_by_name(user_input).id]


def check_condition(user, new_association, picked_plant):
    if new_association is None:
        console.print("Error: new_association is not initialized.", style="bold red")
        return
    while True:
        plant = new_association.plant()
        if plant is None:
            console.print("Error: Plant not found.", style="bold red")
        if not plant.is_alive:
            console.print(
                """
                ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣠⣤⣤⣶⣶⣿⣷⣆⠀⠀⠀⠀
                ⠀⠀⠀⢀⣤⣤⣶⣶⣾⣿⣿⣿⣿⣿⡿⣿⣿⣿⣿⣿⡆⠀⠀⠀
                ⠀⢀⣴⣿⣿⣿⣿⣿⣿⡿⠛⠉⠉⠀⠀⠀⣿⣿⣿⣿⣷⠀⠀⠀
                ⣠⣿⣿⣿⣿⣿⣿⣿⣿⣇⠀⠀⢤⣶⣾⠿⢿⣿⣿⣿⣿⣇⠀⠀
                ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠈⠉⠀⠀⠀⣿⣿⣿⣿⣿⡆⠀
                ⢸⣿⣿⣿⣏⣿⣿⣿⣿⣿⣷⠀⠀⢠⣤⣶⣿⣿⣿⣿⣿⣿⣿⡀
                ⠀⢿⣿⣿⣿⡸⣿⣿⣿⣿⣿⣇⠀⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣧
                ⠀⠸⣿⣿⣿⣷⢹⣿⣿⣿⣿⣿⣄⣀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿
                ⠀⠀⢻⣿⣿⣿⡇⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
                ⠀⠀⠘⣿⣿⣿⣿⠘⠻⠿⢛⣛⣭⣽⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿
                ⠀⠀⠀⢹⣿⣿⠏⠀⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠟⠋
                ⠀⠀⠀⠈⣿⠏⠀⣰⣿⣿⣿⣿⣿⣿⠿⠟⠛⠋⠉⠀⠀⠀⠀⠀
                ⠀⠀⠀⠀⠀⠀⢠⡿⠿⠛⠋⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                """,
                style="red",
            )
            console.print(
                f"[bold red]Plant {new_association.plant().name} is no longer alive."
            )
            break
        if plant.phase == "Flower":
            console.print(
                """
            .-.'  '.-.
          .-(   \  /   )-.
         /   '..oOOo..'   "
 ,       \.--.oOOOOOOo.--./
 |\  ,   (   :oOOOOOOo:   )
_\.\/|   /'--'oOOOOOOo'--'"
'-.. ;/| \   .''oOOo''.   /
.--`'. :/|'-(   /  \   )-'
 '--. `. / //'-'.__.'-;
   `'-,_';//      ,  /|
        '((       |\/./_
          \\  . |\; ..-'
           \\ |\: .'`--.
            \\, .' .--'
             ))'_,-'`
       vsn  //-'
           // 
          //
         |/
                """,
                style="yellow",
            )
            console.print(
                f"[bold green]The {new_association.plant().name} is fully grown and produced a seed!!!"
            )
            break
        # click.clear()
        console.print(
            "Your plant is in need of something! What does it need?",
            style="bold underline green on white",
        )
        console.print("1. Does it need moisture? Type: [underline blue]Water[/]")
        console.print("2. Does it need sunlight? Type: [underline yellow]Sunlight[/]")
        console.print(
            "3. Your plant might be satisfied as is! Type: [underline red]Nothing[/]!"
        )
        console.print(
            "4. Would you like to check your plant's status? Type: [underline green]Plant Status[/]"
        )
        console.print("5. Return to the user menu. Type: [underline]Back[/]!")
        selected_condition = input("What does your plant need?: ").capitalize()

        if selected_condition in EXIT_WORDS:
            exit_program()

        if selected_condition in ["Back"]:
            start_game(user, new_association, picked_plant)

        if selected_condition in ["Plant Status"]:
            console.print(f"{new_association.plant()}")

        while selected_condition not in [
            "Water",
            "Sunlight",
            "Nothing",
        ]:
            console.print("Please pick one of the provided options!", style="bold")
            selected_condition = input("What does your plant need?: ").capitalize()

        new_association.update_user_action(selected_condition)
        condition_matched = new_association.is_condition_matched(
            selected_condition, new_association.plant()
        )
        new_association.process_condition(condition_matched)
        if condition_matched:
            console.print(
                """
░░░░░░░░░░░░░░░░░░░░░░█████████
░░███████░░░░░░░░░░███▒▒▒▒▒▒▒▒███
░░█▒▒▒▒▒▒█░░░░░░░███▒▒▒▒▒▒▒▒▒▒▒▒▒███
░░░█▒▒▒▒▒▒█░░░░██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
░░░░█▒▒▒▒▒█░░░██▒▒▒▒▒██▒▒▒▒▒▒██▒▒▒▒▒███
░░░░░█▒▒▒█░░░█▒▒▒▒▒▒████▒▒▒▒████▒▒▒▒▒▒██
░░░█████████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
░░░█▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒██
░██▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒██▒▒▒▒▒▒▒▒▒▒██▒▒▒▒██
██▒▒▒███████████▒▒▒▒▒██▒▒▒▒▒▒▒▒██▒▒▒▒▒██
█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒▒▒████████▒▒▒▒▒▒▒██
██▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
░█▒▒▒███████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
░██▒▒▒▒▒▒▒▒▒▒████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
░░████████████░░░█████████████████
""",
                style="blue",
            )
            console.print(
                f"You selected the correct condition! Your plant is now a {new_association.plant().phase}",
                style="bold",
            )
        else:
            console.print(
                """
          ██████████          
      ████▒▒▒▒▒▒▒▒▒▒████      
    ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██    
  ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██  
  ██▒▒▒▒██▒▒▒▒▒▒▒▒▒▒██▒▒▒▒██  
██▒▒▒▒▒▒▒▒██▒▒▒▒▒▒██▒▒▒▒▒▒▒▒██
██▒▒▒▒▒▒▒▒▒▒██▒▒██▒▒▒▒▒▒▒▒▒▒██
██▒▒▒▒▒▒▒▒████▒▒████▒▒▒▒▒▒▒▒██
██▒▒▒▒▒▒▒▒████▒▒████▒▒▒▒▒▒▒▒██
██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██
  ██▒▒▒▒▒▒▒▒██████▒▒▒▒▒▒▒▒██  
  ██▒▒▒▒▒▒██▒▒▒▒▒▒██▒▒▒▒▒▒██  
    ██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██    
      ████▒▒▒▒▒▒▒▒▒▒████      
          ██████████          

""",
                style="red",
            )
            console.print(
                f"You selected the wrong condition! Your plant is still a {new_association.plant().phase}",
                style="bold",
            )


def view_rules():
    welcome()
    console.print("Your goal is to grow your plant to the fullest.")
    console.print("Here are the basic instructions:")
    console.print("1. Your plant will decide on what it is required to grow.")
    console.print(
        "2. You must guess the correct demand that the plant wants in 3 days."
    )
    console.print("3. If you do not guess within the given days, your plant will die.")
    console.print(
        "4. Your plant information will be stored and you can always go back and lurk your failed attempts."
    )


def delete_user():
    username = input("Confirm your username: ").strip()

    if username.lower() in EXIT_WORDS:
        exit_program()

    if user := User.find_by_name(username):
        user.delete()
        console.print(f"Successfully deleted {username}")
        console.print("Find yourself or create a new user!", style="bold")
        find_or_create_user()

def view_inventory(user):
    inventory = user.plants()
    console.print(inventory)
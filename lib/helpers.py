from models.user import User
from models.plant import Plant
from models.action import Action
from seed import start_program

EXIT_WORDS = ['exit', 'quit', '7']

def welcome():
    print("Plant Provider: Dead or Alive")

def menu():
    print("Please select an option: ")
    print("1. Start the program")
    print("2. View the rules")
    print("3. View scoreboard")
    print("4. Find User")
    print("5. Find Users")
    print("6. Delete User")
    print("7. Exit the program")
    
def exit_program():
    print("Thanks for playing! Come back soon!")
    exit()

def find_or_create_user():
    name = input("Enter your username: ").strip()

    if name.lower() in EXIT_WORDS:
        exit_program()

    user = User.find_by_name(name)

    if user is None:
        new_user = User.create(name)
        print(f"Welcome {new_user.name}!")
        plant_name = input("Enter your plant's name: ").strip()
        
        if plant_name.lower() in EXIT_WORDS:
            exit_program()
            
        new_plant = Plant.create(plant_name)
        print(f"Thank you for purchasing your new plant {new_plant.name}!")
        start_game(new_user)
    else:
        print(f"Welcome back {user.name}! Your plant is waiting for you!")
        start_game(user)

    
def start_game(user):
    start_program()
    check_condition(user)
    
def check_condition(user):
    print("Your plant is in need of something! Here are your options: ")
    print("1. Give water")
    print("2. Give sunlight")
    print("3. Do nothing!")
    print("4. Check plant's status")
    
    selected_condition = input("What would you like to do?: ").strip().lower()
    
    if selected_condition == EXIT_WORDS:
        exit_program()
    
    if selected_condition not in ["give water", "give sunlight", "do nothing", "check plant's status", "1", "2", "3", "4"]:
        print("Please pick one of the provided options!")
        return check_condition(user)
    
    # if selected_condition == check_condition(selected_condition):
    #     Action.advance_phase()
    

def view_rules():
    print("Your goal is to grow your plant to the fullest.")
    print("Here are the basic instructions:")
    print("1. Your plant will randomly decide on what it is required to grow.")
    print("2. You must guess the correct demand that the plant wants in 5 days.")
    print("3. If you do not guess within the given days, your plant will die.")
    print("4. Your plant information will be stored and you can always go back and lurk your failed attempts.")
    
def view_scoreboard():
    pass

def delete_user():
    name = input("Enter your username: ").strip()
    
    if name.lower() in EXIT_WORDS:
        exit_program()
    
    user = User.find_by_name(name)
    if user:
        user.delete()
        print(f"Successfully deleted {user}")
    else:
        print(f"We could not locate {user.name}. Failed to delete.")

def find_user():
    name = input("Enter your username: ").strip()

    if name.lower() in EXIT_WORDS:
        exit_program()

    if user := User.find_by_name(name):
        print(f"You already created an username {name} with us!") if user else print("No username exists")

def find_users():

    if users := User.get_all():
        for user in users:
            print(user)
    else:
        print("There are no users playing this game :(")

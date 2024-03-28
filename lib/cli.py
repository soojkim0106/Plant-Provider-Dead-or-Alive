##! Entry Point
#! How our menu should look like
from helpers import(
    welcome,
    menu,
    find_or_create_user,
    view_rules,
    view_plants,
    exit_program
)

EXIT_WORDS = ["4", "exit", "quit", "c"]

def main():
    welcome()
    while True:
        menu()
        choice = input('> ')
        if choice in EXIT_WORDS:
            exit_program()
        elif choice == '1':
            find_or_create_user()
        elif choice == '2':
            view_rules()
        elif choice == '3':
            view_plants()
        elif choice == '4':
            exit_program()
        else:
            print("Invalid input")

if __name__ == "__main__":
    main()

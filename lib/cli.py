##! Entry Point
#! How our menu should look like
from helpers import(
    welcome,
    menu,
    find_or_create_user,
    view_rules,
    view_scoreboard,
    find_user,
    find_users,
    delete_user,
    exit_program
)


def main():
    welcome()
    while True:
        menu()
        choice = input('> ')
        if choice == '1':
            find_or_create_user()
        elif choice == '2':
            view_rules()
        elif choice == '3':
            view_scoreboard()
        elif choice == '4':
            find_user()
        elif choice =='5':
            find_users()
        elif choice == '6':
            delete_user()
        elif choice == '7':
            exit_program()
        else:
            print("Invalid input")

if __name__ == "__main__":
    main()

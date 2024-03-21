
#! How our menu should look like
from .cli_helpers import(
    #welcome text
    welcome,
    #Display all the menu below
    menu,
    #Create or find user
    #If no user found, create user and generate another menu that creates plant
    find_or_create_user,
    #Review the rules of the game 
    view_rules,
    #Review the score of current and other players
    view_scoreboard, #! (TBD)
    #Be able to delete user information
    delete_user,
    #Need exit keyword to exit our of the program at any point
    exit_program,
)
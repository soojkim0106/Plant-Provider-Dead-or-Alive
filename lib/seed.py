from models.user import User
from models.plant import Plant
from models.action import Action
# from helpers import console #! FROM RICH

def drop_table():
    pass

def create_table():
    pass

def seed_plantsy():
    pass

def start_program():
    drop_table()
    create_table()
    seed_plantsy()
    # console.print('Back to home page!')

if __name__ == "__main__":
    start_program()
    print('Successfully seeded')

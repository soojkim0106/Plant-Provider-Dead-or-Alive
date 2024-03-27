from models.user import User
from models.plant import Plant
from models.action import Action
import ipdb


# from helpers import console #! FROM RICH


def drop_tables():
    Action.drop_table()
    Plant.drop_table()
    User.drop_table()


def create_tables():
    User.create_table()
    Plant.create_table()
    Action.create_table()


def seed_plantsy():

    user1 = User.create("Bob")
    user2 = User.create("Jane")

    plant1 = Plant.create("bonsai")
    plant2 = Plant.create("Blossom")
    plant3 = Plant.create("Sunflower")

    action1 = Action.create("Water", user1.id, plant1.id)
    action2 = Action.create("Action 2", user1.id, plant2.id)
    action3 = Action.create("Action 2", user2.id, plant3.id)
    
    # ipdb.set_trace()

def start_program():
    drop_tables()
    create_tables()
    seed_plantsy()



if __name__ == "__main__":
    start_program()
    print("Successfully seeded")

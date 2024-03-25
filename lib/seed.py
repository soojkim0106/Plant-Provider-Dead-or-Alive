from models.user import User
from models.plant import Plant
from models.action import Action

# from helpers import console #! FROM RICH


def drop_table():
    User.drop_table()
    Plant.drop_table()
    Action.drop_table()


def create_table():
    User.create_table()
    Plant.create_table()
    Action.create_table()


def seed_plantsy():

    user1 = User.create("Bob")
    user2 = User.create("Jane")

    plant1 = Plant.create("Bob's plant")
    plant2 = Plant.create("Bob's plant1")
    plant3 = Plant.create("Jane's plant")

    action1 = Action.create("Action 1", user1.id, plant1.id)
    action2 = Action.create("Action 2", user1.id, plant2.id)
    action3 = Action.create("Action 2", user2.id, plant3.id)


def start_program():
    drop_table()
    create_table()
    seed_plantsy()


if __name__ == "__main__":
    start_program()
    print("Successfully seeded")

from models.__init__ import CONN, CURSOR
from models.action import Action
from models.plant import Plant
from models.user import User
import ipdb;

Action.drop_table()
User.drop_table()
Plant.drop_table()

User.create_table()
Plant.create_table()
Action.create_table()

user1 = User('Bob Owner')
user1.save()
plant1 = Plant("bob")
plant1.save()

action1 = Action("Need Water", user1.id, plant1.id)
action1.save()
action1.compare_condition("Need Water")

ipdb.set_trace()
from models.__init__ import CONN, CURSOR
from models.action import Action
from models.plant import Plant
from models.user import User

User.drop_table()
Plant.drop_table()

User.create_table()
Plant.create_table()

plant1 = Plant("bob")
plant1.save()
import ipdb; ipdb.set_trace()
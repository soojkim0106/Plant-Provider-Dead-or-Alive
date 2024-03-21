from models.__init__ import CONN, CURSOR
class User:
    def __init__(self, name, id=None):
        self.name = name
        self.id = id
    
    def __repr__(self):
        return f"User {self.id}: {self.name}"

#! Properties and Attributes
    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str):
            raise TypeError('Name must be a string')
        elif len(new_name) < 2:
            raise ValueError('Name must be 2 or more characters')
        else:
            self._name = new_name

#!Association Methods

#! ORM class methods
@classmethod
def create_table(cls):
    CURSOR.execute
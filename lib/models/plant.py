from models.__init__ import CONN, CURSOR
import random
class Plant:
    
    all = []
    phases = ["Seed", "Bud", "Sapling", "Flower"]

    def __init__(self, name, id=None):
        self.name = name
        self._condition = self._random_condition()
        self._phase = 'Seed'
        self.is_alive = True
        self.id = id
        
    def __repr__(self):
        return f"<Plant {self.id}: {self.name}, {self._phase}, {self._condition}, {self.is_alive}>"
    
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

#!Methods
    def update_phase(self, new_phase):
        if new_phase in self.phases:
            self._phase = new_phase
        else:
            raise ValueError('Invalid phase')
    # def condition(self, condition):
    #     plant_condition = self._random_condition()
    #     if condition is not plant_condition:
    #         raise TypeError('Condition must be one of the following in the list')
    #     else:
    #         self._condition = condition

    # def phase(self, phase): #updating seed phase
    #     list_of_next_phase = ['Sapling', 'Bigger Sapling', 'Flower']
    #     if phase not in list_of_next_phase:
    #         raise TypeError('Phase must be one of the following in the list')
    #     else:
    #         self._phase = phase
    
    # def current_phase(self):
    #     return self.phases[self._phase_index]
#! Method to calculate random value
    def _random_condition(self):
        list_of_condition = ['Need Water', 'Need Sunlight', 'Nothing']
        return random.choice(list_of_condition)

    @classmethod
    def instance_from_db(cls, row):
        try:
            plant = cls(row[1], row[0])
            cls.all[plant.id] = plant
            return plant
        except Exception as e:
            print("Error fetching user from database:", e)

    @classmethod
    def get_all(cls):
        try:
            with CONN:
                CURSOR.execute(
        """
            SELECT * FROM plants;
        """
                )
                plants = CURSOR.fetchall()
                return [cls.instance_from_db(plant) for plant in plants]
        except Exception as e:
            print("Error fetching all plants:", e)

    @classmethod
    def find_by_name(cls, name):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        SELECT * FROM plants 
                        WHERE name = ?;
                    """,
                    (name,)
                )
                plant = CURSOR.fetchone()
                return cls.instance_from_db(plant) if plant else None
        except Exception as e:
            print("Error fetching plant by name:", e)

    @classmethod
    def find_by_id(cls, id):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        SELECT * FROM plants 
                        WHERE id = ?;
                    """,
                    (id,)
                )
                plant = CURSOR.fetchone()
                return cls.instance_from_db(plant) if plant else None
        except Exception as e:
            print("Error fetching plant by id:", e)
        


#!Association Methods



p = Plant('Bob')
print(p)
print(f'{p.name} is a {p._phase} and wants {p._random_condition()}')
print(p._phase())
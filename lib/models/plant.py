import random
class Plant:
    
    all = []
    # phase = ["Seed", "Bud", "Sapling", "Flower"]

    def __init__(self, name, id=None):
        self.name = name
        self._condition = self._random_condition()
        # self._phase_index = phase[0]
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
    
    # def change_phase(self): #updating seed phase based on conditional 
    #     # if self is x:
    #         # change phase to bud
    #     # elif self is y:
    #         # change phase to sapling
    #     # elif self is z:
    #         #change phase to flower
    #     pass

    # def check_condition(self):
    #     pass

        


#!Association Methods



p = Plant('Bob')
print(p)
print(f'{p.name} is a {p._phase} and wants {p._random_condition()}')
print(p.phase())
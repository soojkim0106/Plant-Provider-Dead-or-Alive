class Plant:
    
    all = []

    def __init__(self, name, phase, condition, id=None):
        self.name = name
        self.phase = phase
        self.condition = condition
        self.id = id
    
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
    
    @property
    def phase(self):
        return self._phase
    
    @phase.setter
    def phase(self, phase):
        list_of_phase = ['Seed', 'Sappling', 'Bigger Sappling', 'Flower']
        if not isinstance(phase, list_of_phase):
            raise TypeError('Phase must be one of the following in the list')
        else:
            self._phase = phase
    
    @property
    def condition(self):
        return self._condition
    
    @condition.setter
    def condition(self, condition):
        list_of_condition = ['Need Water', 'Need Sunlight', 'Nothing']
        if not isinstance(condition, list_of_condition):
            raise TypeError('Condition must be one of the following in the list')
        else:
            self._condition = condition

#!Association Methods
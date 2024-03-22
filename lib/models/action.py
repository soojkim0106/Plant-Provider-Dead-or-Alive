class Action:
    phases = ["Seed", "Bud", "Sapling", "Flower"]

    def __init__(self, user_id, plant_id, day, plant_phase, id=None):
        self.user_id = user_id
        self.plant_id = plant_id
        self.day = day
        self.plant_phase = plant_phase
        self.wrong_attempts = 0
        self._phase_index = self.phases.index(plant_phase)
        self.id = id

    def __repr__(self):
        return (
            f"<Action {self.id}: {self.day},"
            + f"User ID: {self.user_id},"
            + f"Plant ID: {self.plant_id}>"
        )

    #! Properties and Attributes
    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, day):
        if  0 < day >= 5:
            self._day = day
        else:
            raise ValueError('Day must be greater than 0 and less than or equal to five')

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        from models.user import User
        if not isinstance(user_id, int):
            raise TypeError('user_id must be an integer')
        elif user_id < 1 or not User.find_by_id(user_id): #! Build Find_By_Id in USER
            raise ValueError('User ID must be a positive integer and points to existing user')
        else:
            self._user_id = user_id

    @property
    def plant_id(self):
        return self._plant_id

    @plant_id.setter
    def plant_id(self, plant_id):
        from models.plant import Plant
        if not isinstance(plant_id, int):
            raise TypeError('plant_id must be an integer')
        elif plant_id < 1 or not Plant.find_by_id(plant_id): #! confirm find_by_id in PLANT works
            raise ValueError('Plant ID must be a positive integer and points to existing plant')
        else:
            self._plant_id = plant_id

    @property
    def plant_phase(self):
        return self._plant_phase

    # @plant_phase.setter
    # def plant_phase(self, plant_phase):
    #     from models.plant import Plant
    #     if not isinstance(plant_phase, int):
    #         raise TypeError('plant_phase must be an integer')
    #     elif plant_phase < 1 or not Plant.find_by_phase(plant_phase): #! Build Find_By_Phase in PLANT MAKE DICTIONARY
    #         raise ValueError('Plant phase must be a positive integer and points to existing phase')
    #     else:
    #         self._plant_phase = plant_phase

    @plant_phase.setter
    def plant_phase(self, plant_phase):
        from models.plant import Plant
        if not isinstance(plant_phase, str):
            raise TypeError('plant_phase must be a string')
        elif plant_phase not in self.phases:
            raise ValueError('Plant phase must be a valid phase')
        else:
            self._plant_phase = plant_phase
            self._phase_index = self.phases.index(plant_phase)

    #!Association

    def check_condition(self, user_condition):
        from models.plant import Plant
        plant = Plant.find_by_id(self.plant_id)
        if self.is_dead():
            return "The plant died!!!"
        elif user_condition == plant._condition:
            return self.advance_phase()
        else:
            return self.incorrect_condition()

    def advance_phase(self):
        from models.plant import Plant
        plant = Plant.find_by_id(self.plant_id)
        if self._phase_index < len(self.phases) - 1:
            self._phase_index += 1
            self.plant_phase = self.phases[self._phase_index]
            plant.update_phase(self.plant_phase)
        else:
            return "The plant is fully grown!!!." #! ASCII ART? 

    def incorrect_condition(self):
        self.wrong_attempts += 1  #! ASCII ART RETURNS?
        if self.wrong_attempts >= 5:
            return self.is_dead()

    def is_dead(self):
        from models.plant import Plant
        plant = Plant.find_by_id(self.plant_id)
        if self.wrong_attempts >= 5:
            plant.is_alive = False
            print(f"Plant {plant.name} is no longer alive.") #! this part in CLI helpers?
            return True
        else:
            return False

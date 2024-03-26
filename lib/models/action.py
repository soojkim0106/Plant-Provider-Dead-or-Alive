from models.__init__ import CONN, CURSOR
from models.plant import Plant
from models.user import User
from sqlite3 import IntegrityError
# import ipdb


class Action:

    all = {}

    phases = ["Purchased", "Seed", "Bud", "Sapling", "Flower"]

    def __init__(
        self, user_action, user_id, plant_id, day=1, phase_index=0, plant_phase="Purchased", id=None
    ):
        self.user_action = user_action
        self.user_id = user_id
        self.plant_id = plant_id
        self.day = day
        self.phase_index = phase_index
        self.plant_phase = plant_phase
        self.id = id

    def __repr__(self):
        return (
            f"<Action {self.id}: Day: {self.day} Action: {self.user_action},"
            + f"User ID: {self.user_id},"
            + f"Plant ID: {self.plant_id},"
            + f"Phase Index: {self.phase_index},"
            + f"Phase: {self.plant_phase}>"
        )

    #! Properties and Attributes
    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, day):
        if day <= 4:
            self._day = day
        else:
            raise ValueError(
                "Day must be greater than 0 and less than or equal to five"
            )

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, user_id):
        if not isinstance(user_id, int):
            raise TypeError("user_id must be an integer")
        elif user_id < 1 or not User.find_by_id(user_id):  #! Build Find_By_Id in USER
            raise ValueError(
                "User ID must be a positive integer and points to existing user"
            )
        else:
            self._user_id = user_id

    @property
    def plant_id(self):
        return self._plant_id

    @plant_id.setter
    def plant_id(self, plant_id):
        if not isinstance(plant_id, int):
            raise TypeError("plant_id must be an integer")
        elif plant_id < 1 or not Plant.find_by_id(
            plant_id
        ):  #! confirm find_by_id in PLANT works
            raise ValueError(
                "Plant ID must be a positive integer and points to existing plant"
            )
        else:
            self._plant_id = plant_id

    @property
    def plant_phase(self):
        return self._plant_phase

    @plant_phase.setter
    def plant_phase(self, plant_phase):

        if not isinstance(plant_phase, str):
            raise TypeError("plant_phase must be a string")
        elif plant_phase not in type(self).phases:
            raise ValueError("Plant phase must be a valid phase")
        else:
            self._plant_phase = plant_phase
            self.phase_index = self.phases.index(
                plant_phase
            )  #! can separate properties and attributes

    @property
    def user_action(self):
        return self._user_action

    @user_action.setter
    def user_action(self, user_action):
        if not isinstance(user_action, str):
            raise TypeError(
                "user_action must be a string"
            )  #! We have to validate this somewhere ["Water", "Sunlight", "Nothing"]
        else:
            self._user_action = user_action

    #! Association Methods
    def user(self):
        return User.find_by_id(self.user_id) if self.user_id else None

    def plant(self):
        return Plant.find_by_id(self.plant_id) if self.plant_id else None

    #! Helper Methods

    def start_phase(self):
        if type(self).user_action == "Purchased":
            self.compare_condition()

    def compare_condition(self, user_action):

        plant = Plant.find_by_id(self.plant_id)
        if user_action == plant._condition:
            return self.advance_phase()
        else:
            return self.incorrect_condition()
        
    def advance_phase(self):
        plant = Plant.find_by_id(self.plant_id)
        if self.phase_index < len(self.phases) - 1:
            phase_index = self.phase_index + 1  # sourcery skip: extract-method #! Refractor
            new_phase = type(self).phases[phase_index]
            plant.update_phase(new_phase)
            
            self.phase_index = phase_index
            self.plant_phase = new_phase
            self.day = 1
            type(self).update(self)
        else:
            return "The plant is fully grown and produced a seed!!!"  #! ASCII ART?
        
    def incorrect_condition(self):
        self.day += 1 
        self.update()
        if self.day > 3:
            return self.make_dead()
    def make_dead(self):
        try:
            plant = Plant.find_by_id(self.plant_id)
            plant.is_alive = False
            plant.update()
            return f"Plant {plant.name} is no longer alive."  #! this part in CLI helpers?
        except Exception as e:
            print('Your plant didn\'t die successfully', e)
            
    # def compare_condition(self, user_action):
    #     plant = Plant.find_by_id(self.plant_id)
    #     # if plant._condition == "Planted" or user_action == plant._condition:
    #     if type(self).user_action == plant._condition:
    #         return type(self).advance_phase()
    #     else:
    #         return type(self).incorrect_condition(self)

    # def advance_phase(self):

    #     plant = Plant.find_by_id(self.plant_id)
    #     if self.phase_index < len(self.phases) - 1:
    #         phase_index = self.phase_index + 1  # sourcery skip: extract-method #! Refractor
    #         new_phase = type(self).phases[phase_index]
    #         plant.update_phase(new_phase)

    #         self.phase_index = phase_index
    #         self.plant_phase = new_phase
    #         self.day = 1
    #         type(self).update(self)
    #     else:
    #         return "The plant is fully grown and produced a seed!!!"  #! ASCII ART?

    # def incorrect_condition(self):
    #     type(self).day += 1  #! ASCII ART RETURNS?
    #     if self.day > 5:
    #         return self.make_dead()

    # def make_dead(self):
    #     try:
    #         plant = Plant.find_by_id(self.plant_id)
    #         plant.is_alive = False
    #         plant.update()
    #         return f"Plant {plant.name} is no longer alive."  #! this part in CLI helpers?
    #     except Exception as e:
    #         print('Your plant didn\'t die successfully', e)

    # def update_user_action(self, new_action):
    #     type(self).user_action = new_action
    #     # type(self).update(self)

    #! Utility ORM Class Methods
    @classmethod
    def create_table(cls):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        CREATE TABLE IF NOT EXISTS actions (
                            id INTEGER PRIMARY KEY,
                            user_action TEXT NOT NULL,
                            user_id INTEGER,
                            plant_id INTEGER,
                            day INTEGER,
                            phase_index INTEGER,
                            plant_phase TEXT,
                            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE cascade,
                            FOREIGN KEY (plant_id) REFERENCES plants(id) ON DELETE cascade
                        );
                    """
                )
        except Exception as e:
            return print("Error creating actions table:", e)

    @classmethod
    def drop_table(cls):
        try:
            with CONN:
                CURSOR.execute(
                    """
                    DROP TABLE IF EXISTS actions;
                """
                )
        except Exception as e:
            return e

    @classmethod
    def create(cls, user_action, user_id, plant_id):
        try:
            with CONN:
                new_action = cls(user_action, user_id, plant_id)
                new_action.save()
                return new_action
        except Exception as e:
            print("Error creating new action:", e)

    @classmethod
    def instance_from_db(cls, row):
        try:
            plant = cls(row[1], row[2], row[3], row[4], row[5], row[6], row[0])
            cls.all[plant.id] = plant
            return plant
        except Exception as e:
            print("Error fetching plant from database:", e)

    @classmethod
    def get_all(cls):
        try:
            with CONN:
                CURSOR.execute(
                    """
            SELECT * FROM actions;
        """
                )
                actions = CURSOR.fetchall()
                return [cls.instance_from_db(user_action) for user_action in actions] #! Should be user_action arg?
        except Exception as e:
            print("Error fetching all actions:", e)

    @classmethod
    def find_by_user_action(cls, user_action):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        SELECT * FROM actions 
                        WHERE user_action = ?;
                    """,
                    (user_action,),
                )
                user_action = CURSOR.fetchone()
                return cls.instance_from_db(user_action) if user_action else None
        except Exception as e:
            print("Error fetching plant by action:", e)

    @classmethod
    def find_by_id(cls, id):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        SELECT * FROM actions 
                        WHERE id = ?;
                    """,
                    (id,),
                )
                user_action = CURSOR.fetchone()
                return cls.instance_from_db(user_action) if user_action else None
        except Exception as e:
            print("Error fetching action by id:", e)

    #! ORM instance method
    def save(self):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        INSERT INTO actions (user_action, user_id, plant_id, day, phase_index, plant_phase)
                        VALUES (?,?,?,?,?,?);
                    """,
                    (self.user_action, self.user_id, self.plant_id, self.day, self.phase_index, self.plant_phase),
                )
                self.id = CURSOR.lastrowid
                type(self).all[self.id] = self
                return self
        except IntegrityError as e:
            print("User_Action must be provided")
        except Exception as e:
            print("We could not save this action:", e)

    def update(self):
        try:
            with CONN:
                CURSOR.execute(
                    """
                    UPDATE actions SET user_action = ?, user_id = ?, plant_id = ?, day = ?, phase_index = ?, plant_phase = ?
                    WHERE id = ? 
                    """, (self.user_action, self.user_id, self.plant_id, self.day, self.phase_index, self.plant_phase, self.id,),
                )
            type(self).all[self.id] = self
            return self
        except Exception as e:
            print('Error updating action:', e)

    def delete(self):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        DELETE FROM actions WHERE id =?;
                    """,
                    (self.id,),
                )
                CONN.commit()
                del type(self).all[self.id]
                self.id = None
        except Exception as e:
            print("We could not delete this action:", e)

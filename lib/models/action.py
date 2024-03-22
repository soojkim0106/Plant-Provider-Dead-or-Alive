from models.__init__ import CONN, CURSOR
from sqlite3 import IntegrityError


class Action:
    phases = ["Seed", "Bud", "Sapling", "Flower"]

    def __init__(
        self, user_action, user_id, plant_id, day=0, phase_index=0, plant_phase="Seed", id=None
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
            f"<Action {self.id}: {self.day} {self.user_action},"
            + f"User ID: {self.user_id},"
            + f"Plant ID: {self.plant_id}"
            + f"Phase Index: {self.phase_index}"
            + f"Phase: {self.plant_phase}>"
        )

    #! Properties and Attributes
    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, day):
        if 0 < day >= 5:
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
        from models.user import User

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
        from models.plant import Plant

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

    # @property
    # def phase_index(self):
    #     return self._phase_index

    # @phase_index.setter
    # def phase_index(self, phase_index, plant_phase):
    #     if not isinstance(phase_index, int):
    #         raise TypeError("phase_index must be an integer")
    #     elif phase_index < 0 or phase_index > len(self.phases) - 1:
    #         raise ValueError("Phase index must be between 0 and the number of phases")
    #     else:
    #         self.phase_index = self.phases.index(plant_phase)
    @property
    def user_action(self):
        return self._user_action

    @user_action.setter
    def user_action(self, user_action):
        if not isinstance(user_action, str):
            raise TypeError(
                "user_action must be a string"
            )  #! We need to validate this somewhere ["Need Water", "Need Sunlight", "Nothing"]
        else:
            self._user_action = user_action

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
        if self.phase_index < len(self.phases) - 1:
            self.phase_index += 1
            self.plant_phase = self.phases[self.phase_index]
            plant.update_phase(self.plant_phase)
        else:
            return "The plant is fully grown!!!."  #! ASCII ART?

    def incorrect_condition(self):
        self.day += 1  #! ASCII ART RETURNS?
        if self.day > 4:
            return self.is_dead()

    def is_dead(self):
        from models.plant import Plant

        plant = Plant.find_by_id(self.plant_id)
        # if self.incorrect_condition():
        plant.is_alive = False
        print(f"Plant {plant.name} is no longer alive.")  #! this part in CLI helpers?
        #     return True
        # else:
        #     return False

    @classmethod
    def create_table(cls):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        CREATE TABLE IF NOT EXISTS actions (
                            id INTEGER PRIMARY KEY,
                            user_action TEXT NOT NULL,
                            user_id INTEGER CHECK(user_id > 0),
                            plant_id INTEGER CHECK(plant_id > 0),
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
                new_action = cls(user_action, user_id, plant_id, day=0, phase_index=0)
                new_action.save()
                return new_action
        except Exception as e:
            print("Error creating new action:", e)

    @classmethod
    def instance_from_db(cls, row):
        try:
            plant = cls(row[1], row[2], row[3], row[4], row[0])
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
                return [cls.instance_from_db(plant) for plant in actions]
        except Exception as e:
            print("Error fetching all actions:", e)

    @classmethod
    def find_by_name(cls, name):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        SELECT * FROM actions 
                        WHERE name = ?;
                    """,
                    (name,),
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
                        SELECT * FROM actions 
                        WHERE id = ?;
                    """,
                    (id,),
                )
                plant = CURSOR.fetchone()
                return cls.instance_from_db(plant) if plant else None
        except Exception as e:
            print("Error fetching plant by id:", e)

    #! ORM instance method

    def save(self):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        INSERT INTO actions (name, condition, phase, is_alive)
                        VALUES (?,?,?,?);
                    """,
                    (self.name, self.random_condition(), self.phase, self.is_alive),
                )
                self.id = CURSOR.lastrowid
                type(self).all[self.id] = self
                return self
        except IntegrityError as e:
            print("Name must be provided")
        except Exception as e:
            print("We could not save this plant:", e)

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
            print("We could not delete this plant:", e)

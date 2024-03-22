from models.__init__ import CONN, CURSOR
from sqlite3 import IntegrityError
import random
import ipdb

class Plant:

    all = {}
    phases = ["Seed", "Bud", "Sapling", "Flower"]

    def __init__(
        self,
        name,
        condition= "Need Water",
        is_alive=True,
        phase="Seed",
        id=None,
    ):
        self.name = name
        self.condition = condition
        self.phase = phase
        self.is_alive = is_alive
        self.id = id

    def __repr__(self):
        return f"<Plant {self.id}: {self.name}, {self.phase}, {self.condition}, {self.is_alive}>"

    #! Properties and Attributes
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        if not isinstance(new_name, str):
            raise TypeError("Name must be a string")
        elif len(new_name) < 2:
            raise ValueError("Name must be 2 or more characters")
        else:
            self._name = new_name

    #!Methods
    def update_phase(self, new_phase):
        if new_phase in self.phases:
            self._phase = new_phase
        else:
            raise ValueError("Invalid phase")
    @property
    def condition(self):
        return self._condition

    @condition.setter
    def condition(self, _):
        plant_condition = self.random_condition()
        self._condition = plant_condition

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, phase): #updating seed phase 
        if phase not in type(self).phases:
            raise TypeError('Phase must be one of the following in the list')
        else:
            self._phase = phase

    # def current_phase(self):
    #     return self.phases[self._phase_index]
    #! Method to calculate random value
    def random_condition(self):
        list_of_condition = ["Need Water", "Need Sunlight", "Nothing"]
        return random.choice(list_of_condition)

    @classmethod
    def create_table(cls):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        CREATE TABLE IF NOT EXISTS plants (
                            id INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            condition TEXT,
                            phase TEXT NOT NULL,
                            is_alive BOOLEAN NOT NULL
                        );
                    """
                )
        except Exception as e:
            return e

    @classmethod
    def drop_table(cls):
        try:
            with CONN:
                CURSOR.execute(
                    """
                    DROP TABLE IF EXISTS plants;
                """
                )
        except Exception as e:
            return e

    @classmethod
    def create(cls, name):
        try:
            with CONN:
                new_plant = cls(name, is_alive=True)
                new_plant.save()
                return new_plant
        except Exception as e:
            print("Error creating new plant:", e)

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
                        SELECT * FROM plants 
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
                        INSERT INTO plants (name, condition, phase, is_alive)
                        VALUES (?,?,?,?);
                    """,
                    (
                        self.name,
                        self.random_condition(),
                        self.phase,
                        self.is_alive
                    )
                )
                self.id = CURSOR.lastrowid
                type(self).all[self.id] = self
                return self
        except IntegrityError as e:
            print("Name must be provided")
        except Exception as e:
            print("We could not save this plant:", e)

    def update(self):
        try:
            with CONN:
                CURSOR.execute(
                    """
                    UPDATE actions SET name = ?, condition = ?, is_alive = ?, phase = ?
                    WHERE id = ? 
                    """, (self.name, self.condition, self.is_alive, self.phase),
                )
            type(self).all[self.id] = self
            return self
        except Exception as e:
            print('Error updating plant:', e)
            
    def delete(self):
        try:
            with CONN:
                CURSOR.execute(
                    """
                        DELETE FROM plants WHERE id =?;
                    """,
                    (self.id,),
                )
                CONN.commit()
                del type(self).all[self.id]
                self.id = None
        except Exception as e:
            print("We could not delete this plant:", e)


#!Association Methods
if __name__ == '__main__':
    p = Plant("Bob")
    print(p)
    print(f"{p.name} is a {p.phase} and wants {p.random_condition()}")
    print(p.phase)

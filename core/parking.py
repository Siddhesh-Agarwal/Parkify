import numpy as np
import os
import sqlite3 as sql
from typing import Union, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ParkingData(BaseModel):
    vehicle_type: str
    reg_no: str
    timestamp: datetime = Field(default_factory=datetime.now)
    slot_no: Any


class Parking:
    def __init__(self, n: int, m: int, floors: int = 1):
        """
        key:
            0 - empty
            1 - occupied
        """
        # load the parking lot in a numpy array if it exists
        if os.path.isfile("./parking_lot.npy"):
            self.parking_lot = np.load("./parking_lot.npy")
        else:
            self.parking_lot = np.zeros((n, m, floors), dtype=np.int8)
        # load the database if it exists
        self.conn = sql.connect("./db/parking.db")
        self.cursor = self.conn.cursor()
        if not os.path.isfile("./db/parking.db"):
            # self.conn = sql.connect("./db/parking.db")
            # self.cursor = self.conn.cursor()
            self.cursor.execute(
                """
                CREATE TABLE parking_data(
                    vehicle_type TEXT,
                    reg_no TEXT,
                    timestamp DATETIME,
                    slot_no TEXT
                )
                """
            )
            self.conn.commit()

    def total_slots(self) -> int:
        """Returns the total number of slots in the parking lot"""
        return self.parking_lot.size

    def occupied_slots(self) -> int:
        """Returns the number of occupied slots in the parking lot"""
        return np.sum(self.parking_lot)

    def vacant_slots(self) -> int:
        """Returns the number of vacant slots in the parking lot"""
        return self.total_slots() - self.occupied_slots()

    def get_slot(self) -> Union[int, None]:
        """Returns the first vacant slot in the parking lot"""
        if self.vacant_slots() > 0:
            for i in range(self.parking_lot.shape[0]):
                for j in range(self.parking_lot.shape[1]):
                    for k in range(self.parking_lot.shape[2]):
                        if self.occupy(i, j, k):
                            return i, j, k
        return None

    def occupy(self, n: int, m: int, floors: int = 1) -> bool:
        """occupy a slot in the parking lot"""
        if self.parking_lot[n, m, floors] == 0:
            self.parking_lot[n, m, floors] = 1
            np.save("parking_lot.npy", self.parking_lot)
            return True
        return False

    def vacate(self, n: int, m: int, floors: int = 1) -> bool:
        """Vacate a slot in the parking lot"""
        if self.parking_lot[n, m, floors] == 1:
            self.parking_lot[n, m, floors] = 0
            np.save("parking_lot.npy", self.parking_lot)
            return True
        return False

    def add_to_db(self, data: ParkingData):
        self.cursor.execute(
            """
            INSERT INTO parking_data VALUES(?, ?, ?, ?)
            """,
            (data.vehicle_type, data.reg_no, data.timestamp, data.slot_no),
        )
        self.conn.commit()

    def fetch_slot(self, reg_no: str) -> Union[str, None]:
        self.cursor.execute(
            """
            SELECT slot_no FROM parking_data WHERE reg_no = ?
            """,
            (reg_no,),
        )
        slot = self.cursor.fetchone()
        if slot:
            return slot[0]
        return None

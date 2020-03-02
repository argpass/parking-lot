from typing import List

from parkinglot.domain.models import ParkingBoy
from parkinglot.domain.repositories import ParkingBoyRepo


class ParkingBoyRepoInMem(ParkingBoyRepo):

    def __init__(self, parking_boys: List[ParkingBoy]):
        self._parking_boy_map = {lot.id: lot for lot in parking_boys}

    def get_by_id(self, _id) -> ParkingBoy:
        return self._parking_boy_map[_id]

    def save(self, parking_boy: ParkingBoy):
        self._parking_boy_map[parking_boy.id] = parking_boy

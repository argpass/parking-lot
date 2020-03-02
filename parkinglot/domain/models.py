from typing import List

from parkinglot.domain.base import EventMixin, Event


class Car(object):
    def __init__(self, plate_number: str):
        self._plate_number = plate_number

    @property
    def plate_number(self):
        return self._plate_number

    def __eq__(self, other):
        return self._plate_number == other.plate_number


class Receipt(object):
    def __init__(self, token):
        self._parking_lot_id = None
        self._token = token
        self._parking_boy_id, self._parking_lot_id, self._plate_number = self._token.split(':')[0:3]

    @property
    def parking_lot_id(self) -> str:
        return self._parking_lot_id

    @property
    def parking_boy_id(self) -> str:
        return self._parking_boy_id

    @property
    def plate_number(self) -> str:
        return self._plate_number

    @property
    def token(self) -> str:
        return self._token

    @classmethod
    def create(cls, parking_boy_id, parking_lot_id, plate_number):
        token = "%s:%s:%s" % (parking_boy_id, parking_lot_id, plate_number)
        return cls(token)


class GetCarEvent(Event):
    def __init__(self, parking_lot, car):
        self._parking_lot = parking_lot
        self._car = car


class ParkingLot(EventMixin):
    def __init__(self, _id, cars: List[Car] = None):
        super(ParkingLot, self).__init__()
        self._cars_map = {car.plate_number: car for car in cars or []}
        self._id = _id

    @property
    def id(self):
        return self._id

    def get_car(self, plate_number) -> Car:
        car = self._cars_map.get(plate_number)
        return car

    def park(self, car):
        self._cars_map[car.plate_number] = car


class ParkingBoy(object):
    def __init__(self, _id, parking_lots: List[ParkingLot]):
        self._id = _id
        self._parking_lot_map = {lot.id: lot for lot in parking_lots}
        self._parking_lots = parking_lots
        self._parking_seq = 0

    @property
    def id(self):
        return self._id

    def _next_lot(self) -> ParkingLot:
        self._parking_seq += 1
        return self._parking_lots[self._parking_seq % len(self._parking_lots)]

    def park(self, car: Car) -> Receipt:
        parking_lot: ParkingLot = self._next_lot()
        parking_lot.park(car)
        return Receipt.create(parking_boy_id=self.id, parking_lot_id=parking_lot.id, plate_number=car.plate_number)

    def get_car(self, receipt: Receipt) -> Car:
        self._assert_is_my_receipt(receipt)
        parking_lot: ParkingLot = self._parking_lot_map[receipt.parking_lot_id]
        return parking_lot.get_car(receipt.plate_number)

    def _assert_is_my_receipt(self, receipt):
        assert receipt.parking_boy_id == self.id

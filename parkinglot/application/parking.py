from parkinglot.domain.models import Receipt, Car, ParkingBoy
from parkinglot.domain.repositories import ParkingBoyRepo


class ParkingCommand(object):
    def __init__(self, parking_boy_id, plate_number):
        self._plate_number = plate_number
        self._parking_boy_id = parking_boy_id

    @property
    def car(self) -> Car:
        return Car(self._plate_number)

    @property
    def parking_boy_id(self):
        return self._parking_boy_id


class GetCarCommand(object):
    def __init__(self, receipt_token: str):
        self._receipt_token = receipt_token

    @property
    def receipt(self) -> Receipt:
        return Receipt(self._receipt_token)


class ParkingLotApplication(object):
    def __init__(self, parking_boy_repo: ParkingBoyRepo):
        self.parking_boy_repo = parking_boy_repo

    def park(self, parking_cmd: ParkingCommand) -> Receipt:
        boy: ParkingBoy = self.parking_boy_repo.get_by_id(parking_cmd.parking_boy_id)
        receipt: Receipt = boy.park(parking_cmd.car)
        self.parking_boy_repo.save(boy)
        return receipt

    def get_car(self, get_car_cmd: GetCarCommand) -> Car:
        parking_boy: ParkingBoy = self.parking_boy_repo.get_by_id(get_car_cmd.receipt.parking_boy_id)
        car = parking_boy.get_car(get_car_cmd.receipt)
        self.parking_boy_repo.save(parking_boy)
        return car


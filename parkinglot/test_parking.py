from parkinglot.application.parking import ParkingLotApplication, ParkingCommand, GetCarCommand
from parkinglot.domain.models import ParkingLot, ParkingBoy, Receipt, Car
from parkinglot.domain.repositories import ParkingBoyRepo
from parkinglot.infra.mem_repositories import ParkingBoyRepoInMem


parking_lots = [ParkingLot("parking_lot_%d" % i) for i in range(3)]
primary_parking_boy = ParkingBoy("parking_boy_no1", parking_lots)
parking_boys = [primary_parking_boy]
parking_boy_repo: ParkingBoyRepo = ParkingBoyRepoInMem(parking_boys)


def test_park_a_car_and_get_the_same_car_with_right_receipt():
    parking_application = ParkingLotApplication(parking_boy_repo)
    car = Car("川W888888")
    receipt: Receipt = parking_application.park(ParkingCommand(primary_parking_boy.id, car.plate_number))
    car_got = parking_application.get_car(GetCarCommand(receipt.token))
    assert car == car_got

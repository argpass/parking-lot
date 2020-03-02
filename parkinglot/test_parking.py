from parkinglot.application.parking import ParkingLotApplication, ParkingCommand, GetCarCommand
from parkinglot.domain.models import ParkingLot, ParkingBoy, Receipt, Car
from parkinglot.domain.repositories import ParkingBoyRepo
from parkinglot.infra.mem_repositories import ParkingBoyRepoInMem


parking_lots = [ParkingLot("parking_lot_%d" % i) for i in range(3)]
primary_parking_boy = ParkingBoy("parking_boy_no1", parking_lots)
parking_boys = [primary_parking_boy]
parking_boy_repo: ParkingBoyRepo = ParkingBoyRepoInMem(parking_boys)


def test_park_cars_and_get_the_same_cars_with_right_receipts():
    parking_application = ParkingLotApplication(parking_boy_repo)
    cars = [Car("川W8888%2d" % i) for i in range(10)]
    receipts = []
    cars_got = []

    # parking
    for car in cars:
        receipt: Receipt = parking_application.park(ParkingCommand(primary_parking_boy.id, car.plate_number))
        receipts.append(receipt)

    # get cars
    for receipt in receipts:
        car_got = parking_application.get_car(GetCarCommand(receipt.token))
        cars_got.append(car_got)

    assert cars == cars_got

from driver import Driver
from passenger import Passenger, PassengerRequest
from ride_sharing_system import RideSharingSystem

def main():
    # Instantiate the RideSharingSystem and add some drivers and passenger requests
    ride_sharing_system = RideSharingSystem()
    ride_sharing_system.drivers = [
        Driver("Bob", (40.7128, -74.0060), True),
        Driver("Alice", (51.5074, -0.1278), True)
    ]
    ride_sharing_system.passenger_request_queue = [
        PassengerRequest(Passenger("John"), (48.8566, 2.3522),
                         (52.5200, 13.4050)),
    ]

    # Process passenger requests
    ride_sharing_system.process_passenger_requests()

    # # Cancel a passenger's request
    # passenger_request_to_cancel = ride_sharing_system.passenger_request_queue[0]
    # ride_sharing_system.cancel_request(passenger_request_to_cancel)

    # # Update a driver's availability
    # driver_to_update = ride_sharing_system.drivers[0]
    # ride_sharing_system.update_driver_status(driver_to_update, False)


if __name__ == "__main__":
    main()

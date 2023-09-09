import uuid
from logger import logger


class Passenger:
    """
    Represents a passenger for a ride-sharing service.

    Attributes:
    - name (str): The name of the passenger.
    """

    def __init__(self, name):
        self.name = name


class PassengerRequest:
    """
    Represents a ride request made by a passenger.

    Attributes:
    - passenger (Passenger): The passenger making the request.
    - pickup_address (str): The address where the passenger needs to be picked up.
    - max_wait_time (int): The maximum amount of time (in minutes) the passenger is willing to wait.
    - is_canceled (bool): Indicates whether the request has been canceled (default is False).
    """

    def __init__(self, passenger, pickup_address, dropoff_address):
        self.passenger = passenger
        self.pickup_address = pickup_address
        self.dropoff_address = dropoff_address
        self.is_canceled = False
        self.uuid = str(uuid.uuid4())
        logger.info(
            f"Passenger request created: UUID - {self.uuid}, Passenger - {self.passenger.name}, Pickup Address - {self.pickup_address}")

    def cancel(self):
        """
        Cancels the passenger's ride request.
        Sets the 'is_canceled' attribute to True.
        """
        self.is_canceled = True
        logger.info(
            f"{self.uuid} Passenger request canceled")

from logger import logger

class Driver:
    """
    Represents a driver for a ride-sharing service.

    Attributes:
    - name (str): The name of the driver.
    - location (str): The current location of the driver.
    - is_available (bool): Indicates whether the driver is available for rides (default is True).
    """

    def __init__(self, name, location, is_available=True):
        """
        Initializes a new driver instance.

        Args:
        - name (str): The name of the driver.
        - location (str): The initial location of the driver.
        - is_available (bool, optional): Indicates whether the driver is available for rides (default is True).
        """
        self.name = name
        self.location = location
        self.is_available = is_available
        logger.info(
            f"Driver created name - {self.name}, location - {self.location}")

    def update_status(self, is_available):
        """
        Updates the driver's availability status.

        Args:
        - is_available (bool): The new availability status of the driver.
        """
        self.is_available = is_available
        logger.info(
            f"{self.uuid} Driver status updated to {self.is_available}")

from math import radians, sin, cos, sqrt, atan2
from logger import logger
import heapq
import time


class RideSharingSystem:
    """
    Represents a ride-sharing system that manages passenger requests and drivers.

    Attributes:
    - passenger_request_queue (list): A queue of pending passenger requests.
    - drivers (list): A list of available drivers.
    - MAX_DISTANCE (float): Maximum distance for driver availability (initialized as positive infinity).
    - AVERAGE_SPEED (float): Average driving speed in kilometers per hour (default is 30.0 km/h).

    Methods:
    - find_available_drivers(passenger_location): Find available drivers near a passenger's location.
    - calculate_distance(location1, location2): Calculate the distance between two locations.
    - get_coordinates(address): Retrieve the coordinates (latitude, longitude) of an address.
    - calculate_estimated_arrival_time(distance): Calculate estimated arrival time based on distance and speed.
    - assign_ride(driver, passenger, optimal_route, distance): Assign a ride to a driver.
    - process_passenger_requests(): Process pending passenger requests.
    - calculate_optimal_route(start_location, end_location): Calculate the optimal route between two locations.
    - cancel_request(passenger_request): Cancel a passenger's ride request.
    - update_driver_status(driver, is_available): Update a driver's availability status.
    """

    passenger_request_queue = []
    drivers = []
    graph = {
        'A': {'B': 1, 'C': 4},
        'B': {'A': 1, 'C': 2, 'D': 5},
        'C': {'A': 4, 'B': 2, 'D': 1},
        'D': {'B': 5, 'C': 1}
    }
    location_mapping = {
        'A': (48.8566, 2.3522),
        'B': (40.7128, -74.0060),
        'C': (51.5074, -0.1278),
        'D': (52.5200, 13.4050)
    }
    MAX_DISTANCE = float('inf')
    AVERAGE_SPEED = 30.0
    RADIUS_OF_EARTH = 6371.0

    def find_available_drivers(self, passenger_location):
        """
        Find available drivers near a passenger's location.

        Args:
        - passenger_location (tuple): The coordinates (latitude, longitude) of the passenger's location.

        Returns:
        - available_drivers (list): A list of available drivers near the passenger.
        """
        available_drivers = []
        for driver in self.drivers:
            if driver.is_available and self.calculate_distance(driver.location, passenger_location) <= self.MAX_DISTANCE:
                available_drivers.append(driver)
        return available_drivers

    def calculate_distance(self, location1, location2):
        """
        Calculate the distance between two locations.

        Args:
        - location1 (tuple): The coordinates (latitude, longitude) of the first location.
        - location2 (tuple): The coordinates (latitude, longitude) of the second location.

        Returns:
        - distance (float): The distance in kilometers between the two locations.
        """
        lat1, lon1 = radians(location1[0]), radians(location1[1])
        lat2, lon2 = radians(location2[0]), radians(location2[1])

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = self.RADIUS_OF_EARTH * c

        return distance

    def get_coordinates(self, address):
        """
        Retrieve the coordinates (latitude, longitude) of an address.

        Args:
        - address (str): The address for which coordinates are needed.

        Returns:
        - coordinates (tuple): The coordinates (latitude, longitude) of the address.
        """
        for location_identifier, location_coordinates in self.location_mapping.items():
            if location_coordinates == address:
                return location_identifier
        return None

    def calculate_estimated_arrival_time(self, distance):
        """
        Calculate estimated arrival time based on distance and speed.

        Args:
        - distance (float): The distance in kilometers.

        Returns:
        - estimated_time (str): Estimated arrival time in minutes (formatted as a string).
        """
        estimated_time_minutes = (distance / self.AVERAGE_SPEED) * 60
        return estimated_time_minutes

    def assign_ride(self, driver, passenger, optimal_route, distance):
        """
        Assign a ride to a driver and update their availability.

        Args:
        - driver (Driver): The driver to assign the ride to.
        - passenger (Passenger): The passenger requesting the ride.
        - optimal_route (list): The optimal route for the ride.
        - distance (float): The distance of the ride in kilometers.
        """
        if driver.is_available:
            # Update driver status
            driver.is_available = False

            # Assign the ride to the driver (you may want to update other ride-related attributes)
            driver.current_passenger = passenger
            driver.current_route = optimal_route
        else:
            # Driver is not available, handle the case accordingly (e.g., put the passenger in a queue)
            self.handle_unavailable_driver(passenger)

    def process_passenger_requests(self):
        """
        Process pending passenger ride requests, matching them with available drivers.
        """
        while self.passenger_request_queue:
            passenger_request = self.passenger_request_queue.pop(0)

            if passenger_request.is_canceled:
                logger.info(
                    f"{passenger_request.uuid} Passenger request canceled")
                continue
            
            logger.info(
                f"{passenger_request.uuid} Processing passenger request {passenger_request}")

            available_drivers = self.find_available_drivers(
                passenger_request.pickup_address)

            best_driver = None
            best_distance = float('inf')
            best_estimated_arrival_time = float('inf')
            passenger_grid_pickup_location = self.get_coordinates(
                passenger_request.pickup_address)

            for driver in available_drivers:
                driver_grid_location = self.get_coordinates(driver.location)
                optimal_route = self.calculate_optimal_route(
                    driver_grid_location, passenger_grid_pickup_location)
                
                # Skip this driver if the optimal route is empty
                if not optimal_route: 
                    self.handle_unavailable_driver(passenger_request)
                    logger.info(
                        f"{passenger_request.uuid} No route found for driver {driver.name}")
                    continue  

                distance_to_pickup = self.calculate_distance(
                    driver.location, passenger_request.pickup_address)
                estimated_arrival_time = self.calculate_estimated_arrival_time(
                    distance_to_pickup)

                if estimated_arrival_time < best_estimated_arrival_time or (
                        estimated_arrival_time == best_estimated_arrival_time and distance_to_pickup < best_distance):
                    best_driver = driver
                    best_distance = distance_to_pickup
                    best_estimated_arrival_time = estimated_arrival_time

            if best_driver is not None:
                logger.info(
                    f"{passenger_request.uuid} Assigned driver for trip {best_driver.name}")
                logger.info(
                    f"{passenger_request.uuid} Optimal route to passenger location {optimal_route}")
                logger.info(
                    f"{passenger_request.uuid} Distance to passenger location {best_distance:.2f}")
                logger.info(
                    f"{passenger_request.uuid} Estimated arrival time to passenger {estimated_arrival_time:.2f} minutes")

                # Assign the ride to the best driver and perform other actions
                self.assign_ride(best_driver, passenger_request,
                                 optimal_route, best_distance)
            else:
                logger.info(
                    f"{passenger_request.uuid} No available drivers found.")
                self.handle_unavailable_driver(passenger_request)

            time.sleep(5)

    def handle_unavailable_driver(self, passenger):
        """
        Handle the case when no available drivers are found.
        Puts the passenger in a queue for future ride requests.

        Args:
        passenger (Passenger): The passenger object.

        Returns:
        None
        """
        self.passenger_request_queue.append(passenger)

    def calculate_optimal_route(self, start_location, end_location):
        """
        Calculate the optimal route between two locations.

        Args:
        - start_location (tuple): The coordinates (latitude, longitude) of the starting location.
        - end_location (tuple): The coordinates (latitude, longitude) of the destination location.

        Returns:
        - optimal_route (list): A list of coordinates representing the optimal route.
        """
        start_node = start_location
        end_node = end_location

        # Initialize distances and predecessors
        distances = {node: float('inf') for node in self.graph}
        predecessors = {node: None for node in self.graph}
        distances[start_node] = 0

        # Priority queue for nodes to visit
        queue = [(0, start_node)]

        while queue:
            current_distance, current_node = heapq.heappop(queue)

            # If we reach the end node, reconstruct the path and return it
            if current_node == end_node:
                path = []
                while current_node:
                    path.append(current_node)
                    current_node = predecessors[current_node]
                return path[::-1]

            # If the current distance is greater than the stored distance, skip
            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight

                # If a shorter path is found, update distances and predecessors
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

        # If no path is found, return None
        return None

    def cancel_request(self, passenger_request):
        """
        Cancel a passenger's ride request.

        Args:
        - passenger_request (PassengerRequest): The passenger request to cancel.
        """
        passenger_request.cancel()

    def update_driver_status(self, driver, is_available):
        """
        Update a driver's availability status.

        Args:
        - driver (Driver): The driver whose availability status needs to be updated.
        - is_available (bool): The new availability status of the driver.
        """
        driver.update_status(is_available)

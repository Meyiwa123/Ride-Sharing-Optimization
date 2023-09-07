'''
Author: Oritsemeyiwa Jordan Temile

Use Case: Ride-Sharing Optimization

Problem Description:
In urban areas, ride-sharing platforms like Uber and Lyft have become increasingly popular as a means of transportation. 
However, they face a significant challenge in optimizing ride assignments and route planning to ensure efficient use of resources, 
minimize passenger wait times, and reduce travel costs for both riders and drivers.

Problem Statement:
Imagine you are a software engineer working for a ride-sharing company. The company operates in a large city with thousands of 
drivers and passengers using the platform daily. The problem at hand is to optimize the ride assignment and route planning process 
to improve the overall efficiency of the system while providing a seamless experience for passengers and drivers.

Key Challenges:
1. Demand and Supply Matching: The platform needs to efficiently match incoming ride requests from passengers with available drivers, 
considering factors like passenger location, driver location, and ride preferences.

2. Route Optimization: Once a ride is assigned, the system needs to calculate the most efficient route for the driver to reach 
the passenger and then the destination while considering real-time traffic conditions.

3. Dynamic Changes: The system should adapt to dynamic changes such as new ride requests, and driver availability in real-time.

4. Fairness and Balance: Ensure fairness in assigning rides to drivers while preventing overburdening certain drivers and 
optimizing overall system efficiency.

5. Customer Experience: Minimize passenger wait times and provide accurate estimated arrival times to enhance the passenger experience.
'''

# Import necessary libraries/modules
from math import radians, sin, cos, sqrt, atan2
import heapq
import time


class RideSharingSystem:
    def __init__(self):
        self.passenger_request_queue = []
        self.graph = self.get_graph()
        self.drivers = []

    # Define data structures to represent drivers and passengers.
    class Driver:
        def __init__(self, id, location):
            self.id = id
            self.location = location
            self.is_available = True

    class Passenger:
        def __init__(self, id, location, destination):
            self.id = id
            self.location = location
            self.destination = destination

    def get_graph(self):
        return {
            'A': {'B': 1, 'C': 4},
            'B': {'A': 1, 'C': 2, 'D': 5},
            'C': {'A': 4, 'B': 2, 'D': 1},
            'D': {'B': 5, 'C': 1}
        }

    def find_available_drivers(self, passenger_location):
        MAX_DISTANCE = float('inf')  # Maximum distance
        available_drivers = []
        for driver in self.drivers:
            # Check if the driver is available and within an acceptable range of the passenger's location
            if driver.is_available and self.calculate_distance(driver.location, passenger_location) <= MAX_DISTANCE:
                available_drivers.append(driver)

        return available_drivers

    def match_passenger_with_driver(self, passenger, available_drivers):
        best_driver = None
        min_distance = float('inf')

        for driver in available_drivers:
            distance = self.calculate_distance(
                driver.location, passenger.location)
            if distance < min_distance:
                best_driver = driver
                min_distance = distance

        return best_driver, distance

    def calculate_distance(self, location1, location2):
        """
        Calculate the distance (in kilometers) between two geographic locations
        using the Haversine formula.

        Args:
        location1 (tuple): Latitude and longitude of the first location in degrees.
        location2 (tuple): Latitude and longitude of the second location in degrees.

        Returns:
        float: The distance in kilometers.
        """
        # Radius of the Earth in kilometers
        R = 6371.0

        # Convert latitude and longitude from degrees to radians
        lat1, lon1 = radians(location1[0]), radians(location1[1])
        lat2, lon2 = radians(location2[0]), radians(location2[1])

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        # Calculate the distance
        distance = R * c

        return distance

    def get_coordinates(self, coordinates):
        """
        Get the location identifier (letter) for given latitude and longitude coordinates.

        Args:
        coordinates (tuple): A tuple containing latitude and longitude coordinates.
        location_mapping (dict): A dictionary mapping location identifiers to coordinates.

        Returns:
        str: The location identifier (e.g., 'A', 'B', 'C', 'D').
        """
        # A dictionary mapping location identifiers to coordinates.
        location_mapping = {
            'A': (48.8566, 2.3522),
            'B': (40.7128, -74.0060),
            'C': (51.5074, -0.1278),
            'D': (52.5200, 13.4050)
        }
        for location_identifier, location_coordinates in location_mapping.items():
            if location_coordinates == coordinates:
                return location_identifier
        return None  # Return None if the location identifier is not found in the mapping

    def calculate_optimal_route(self, driver, passenger, graph):
        """
        Calculate the optimal route using Dijkstra's algorithm.

        Args:
        driver (Driver): The driver object with location information.
        passenger (Passenger): The passenger object with location information.

        Returns:
        list: The optimal route from the driver's location to the passenger's location.
        """
        start_node = self.get_coordinates(driver.location)
        end_node = self.get_coordinates(passenger.location)

        # Initialize distances and predecessors
        distances = {node: float('inf') for node in graph}
        predecessors = {node: None for node in graph}
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

            for neighbor, weight in graph[current_node].items():
                distance = current_distance + weight

                # If a shorter path is found, update distances and predecessors
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    predecessors[neighbor] = current_node
                    heapq.heappush(queue, (distance, neighbor))

        # If no path is found, return an empty list
        return []

    def assign_ride(self, driver, passenger, optimal_route, distance):
        """
        Assign a ride to the driver, update driver status, and notify the passenger.

        Args:
        driver (Driver): The driver object.
        passenger (Passenger): The passenger object.
        optimal_route (list): The optimal route from driver's location to passenger's location.

        Returns:
        None
        """
        if driver.is_available:
            # Update driver status
            driver.is_available = False

            # Assign the ride to the driver (you may want to update other ride-related attributes)
            driver.current_passenger = passenger
            driver.current_route = optimal_route

            # Notify the passenger about the driver's arrival
            message = f"{driver.id} is on the way. Estimated arrival time: {self.calculate_estimated_arrival_time(distance)}"
            self.send_notification(passenger, message)
        else:
            # Driver is not available, handle the case accordingly (e.g., put the passenger in a queue)
            self.handle_unavailable_driver(passenger)

    def calculate_estimated_arrival_time(self, distance):
        """
        Calculate the estimated arrival time based on average speed and distance.

        Args:
        optimal_route (list): The optimal route from the driver's location to the passenger's location.
        average_speed (float): The average speed of the driver in kilometers per hour.

        Returns:
        str: The estimated arrival time in minutes (e.g., "15 minutes").
        """
        average_speed = 30.0  # Average speed in kilometers per hour

        # Calculate the estimated arrival time in minutes
        estimated_time_minutes = (distance / average_speed) * 60

        return f"{estimated_time_minutes:.2f} minutes"

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
        message = "You are in the waiting queue for a ride. We'll notify you when a driver becomes available."
        self.send_notification(passenger, message)

    def send_notification(self, passenger, message):
        """
        Send a notification to the passenger.

        Args:
        passenger (Passenger): The passenger object.
        message (str): The notification message to be sent.

        Returns:
        None
        """
        print(f"Notifying passenger {passenger.id}: {message}")

    def get_next_passenger_request(self):
        """
        Get the next passenger request from the queue without processing it.

        Returns:
        Passenger: The next passenger request in the queue.
        """
        if self.passenger_request_queue:
            return self.passenger_request_queue[0]
        else:
            return None  # Return None if the queue is empty

    def add_passenger(self, id, location, destination):
        """
        Add a new passenger to the system.

        Args:
        id (str): Passenger's unique identifier.
        location (tuple): Latitude and longitude of the passenger's current location.
        destination (tuple): Latitude and longitude of the passenger's destination.

        Returns:
        Passenger: The newly created Passenger object.
        """
        passenger = self.Passenger(id, location, destination)
        self.passenger_request_queue.append(passenger)

    def add_driver(self, id, location):
        """
        Add a new driver to the system.

        Args:
        id (str): Driver's unique identifier.
        location (tuple): Latitude and longitude of the driver's current location.

        Returns:
        Driver: The newly created Driver object.
        """
        driver = self.Driver(id, location)
        self.drivers.append(driver)

    def add_test_data(self):
        """
        Simulate receiving a passenger request.

        Returns:
        Passenger: A new passenger request.
        """
        # Sample driver
        driver_id = "Driver1"
        driver_location = (40.7128, -74.0060)
        (self.add_driver(driver_id, driver_location))

        driver_id = "Driver2"
        driver_location = (51.5074, -0.1278)
        (self.add_driver(driver_id, driver_location))

        # Sample passenger request
        passenger_id = "Passenger1"
        passenger_location = (48.8566, 2.3522)
        passenger_destination = (52.5200, 13.4050)

        # Create a new Passenger object
        self.add_passenger(passenger_id, passenger_location,
                           passenger_destination)

    # Main loop for handling ride requests.
    def main(self):
        # Add test data
        self.add_test_data()
        while True:
            print("Waiting for passenger requests...")
            new_passenger_request = self.get_next_passenger_request()
            print("Processing passenger request...")
            if new_passenger_request:
                available_drivers = self.find_available_drivers(
                    new_passenger_request.location)

                if available_drivers:
                    matched_driver, distance = self.match_passenger_with_driver(
                        new_passenger_request, available_drivers)

                    if matched_driver:
                        optimal_route = self.calculate_optimal_route(
                            matched_driver, new_passenger_request, self.graph)
                        print(
                            f"Optimal route for driver {matched_driver.id}: {optimal_route}")
                        self.assign_ride(matched_driver,
                                         new_passenger_request, optimal_route, distance)
                    else:
                        self.handle_unavailable_driver(new_passenger_request)
            print("Waiting for next request...")

            # Wait for 10 seconds before processing the next request.
            time.sleep(10)


# Example usage:
if __name__ == "__main__":
    ride_sharing_system = RideSharingSystem()
    ride_sharing_system.main()

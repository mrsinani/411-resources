import logging
import math
import os
import time
from typing import List

from racing.models.cars_model import Cars
from racing.utils.logger import configure_logger
from racing.utils.api_utils import get_random


logger = logging.getLogger(__name__)
configure_logger(logger)


class TrackModel:
    """A class to manage the racing track where cars compete.
    """

    def __init__(self):
        """Initializes the TrackModel with an empty list of competing cars.

        The track is initially empty, and the car cache and time-to-live (TTL) caches are also initialized.
        The TTL is set to 60 seconds by default, but this can be overridden by setting the TTL_SECONDS environment variable.

        Attributes:
            track (List[int]): The list of ids of the cars on the track.
            _car_cache (dict[int, Cars]): A cache to store car objects for quick access.
            _ttl (dict[int, float]): A cache to store the time-to-live for each car.
            ttl_seconds (int): The time-to-live in seconds for the cached car objects.
        """
        self.track = []
        self._car_cache = {}
        self._ttl = {}
        self.ttl_seconds = int(os.getenv('TTL_SECONDS', 60))
        logger.info(f"Initialized TrackModel with TTL of {self.ttl_seconds} seconds.")

    def race(self) -> str:
        """Simulates a race between two cars.

        Simulates a race between two cars. Computes their performance scores,
        normalizes the difference, and determines the winner based on a random number.

        Returns:
            str: The make and model of the winning car.

        Raises:
            ValueError: If there are not enough cars on the track.
        """
        if len(self.track) < 2:
            logger.error("There must be two cars to start a race.")
            raise ValueError("There must be two cars to start a race.")

        car_1, car_2 = self.get_cars()

        logger.info(f"Race started between {car_1.make} {car_1.model} and {car_2.make} {car_2.model}")

        perf_1 = self.get_performance_score(car_1)
        perf_2 = self.get_performance_score(car_2)

        logger.debug(f"Performance score for {car_1.make} {car_1.model}: {perf_1:.3f}")
        logger.debug(f"Performance score for {car_2.make} {car_2.model}: {perf_2:.3f}")

        # Compute the absolute performance difference
        # And normalize using a logistic function for better probability scaling
        delta = abs(perf_1 - perf_2)
        normalized_delta = 1 / (1 + math.e ** (-delta / 100))  # Dividing by 100 to prevent extreme differences

        logger.debug(f"Raw delta between performance scores: {delta:.3f}")
        logger.debug(f"Normalized delta: {normalized_delta:.3f}")

        random_number = get_random()

        logger.debug(f"Random number from random.org: {random_number:.3f}")

        # The better performance score gives a higher probability of winning
        # but doesn't guarantee it - random chance is still a factor
        if perf_1 > perf_2:
            win_probability = 0.5 + normalized_delta/2
            if random_number < win_probability:
                winner = car_1
                loser = car_2
            else:
                winner = car_2
                loser = car_1
        else:
            win_probability = 0.5 + normalized_delta/2
            if random_number < win_probability:
                winner = car_2
                loser = car_1
            else:
                winner = car_1
                loser = car_2

        logger.info(f"The winner is: {winner.make} {winner.model}")

        winner.update_stats('win')
        loser.update_stats('loss')

        self.clear_track()

        return f"{winner.make} {winner.model}"

    def clear_track(self):
        """Clears the list of cars from the track.
        """
        if not self.track:
            logger.warning("Attempted to clear an empty track.")
            return
        logger.info("Clearing the cars from the track.")
        self.track.clear()
        logger.info("Track cleared successfully.")

    def enter_track(self, car_id: int):
        """Prepares a car by adding it to the track for an upcoming race.

        Args:
            car_id (int): The ID of the car to enter the track.

        Raises:
            ValueError: If the track already has two cars (race is full).
            ValueError: If the car ID is invalid or the car does not exist.
        """
        if len(self.track) >= 2:
            logger.error(f"Attempted to add car ID {car_id} but the track is full")
            raise ValueError("Track is full. There can only be two cars in a race.")

        try:
            car = Cars.get_car_by_id(car_id)
        except ValueError as e:
            logger.error(str(e))
            raise

        logger.info(f"Adding car '{car.make} {car.model}' (ID {car_id}) to the track")
        self.track.append(car_id)
        
        # Cache the car object with TTL
        self._car_cache[car_id] = car
        self._ttl[car_id] = time.time() + self.ttl_seconds
        
        logger.info(f"Current cars on the track: {[Cars.get_car_by_id(c).make + ' ' + Cars.get_car_by_id(c).model for c in self.track]}")

    def get_cars(self) -> List[Cars]:
        """Retrieves the current list of cars on the track.

        Returns:
            List[Cars]: A list of Cars instances representing the cars on the track.
        """
        if not self.track:
            logger.warning("Retrieving cars from an empty track.")
            return []
        else:
            logger.info(f"Retrieving {len(self.track)} cars from the track.")

        boxers = []
        for car_id in self.track:
            # Check if in cache and not expired
            now = time.time()
            expired = car_id not in self._ttl or self._ttl[car_id] < now
            
            if expired:
                logger.info(f"TTL expired or missing for car {car_id}. Refreshing from DB.")
                car = Cars.get_car_by_id(car_id)
                # Update cache
                self._car_cache[car_id] = car
                self._ttl[car_id] = now + self.ttl_seconds
            else:
                logger.debug(f"Using cached car {car_id} (TTL valid).")
                car = self._car_cache[car_id]
                
            boxers.append(car)

        logger.info(f"Retrieved {len(boxers)} cars from the track.")
        return boxers

    def get_performance_score(self, car: Cars) -> float:
        """Calculates the performance score for a car based on its attributes.

        The performance score is computed using a formula that considers various car attributes.
        - Higher horsepower increases the score
        - Lower weight increases the score (power-to-weight ratio)
        - Lower 0-60 time increases the score (better acceleration)
        - Higher top speed increases the score
        - Better handling increases the score
        - The year of the car slightly affects the score (newer cars tend to perform better)

        Args:
            car (Cars): A Cars instance representing the competing car.

        Returns:
            float: The calculated performance score.
        """
        logger.info(f"Calculating performance score for {car.make} {car.model}: "
                   f"horsepower={car.horsepower}, weight={car.weight}, "
                   f"0-60={car.zero_to_sixty}, top_speed={car.top_speed}, handling={car.handling}")
        
        # Power-to-weight ratio is a key factor in performance
        power_to_weight = car.horsepower / car.weight * 1000
        
        # Better (lower) 0-60 times means better performance, so invert it
        acceleration_factor = 10 / car.zero_to_sixty
        
        # Year factor - newer cars get a slight boost
        year_factor = (car.year - 1950) / 70  # Normalized from 0 to ~1
        
        # Calculate the overall performance score
        # This formula gives a balanced weight to each attribute
        performance = (
            power_to_weight * 0.4 +                 # 40% weight for power-to-weight
            acceleration_factor * 20 +              # Acceleration importance
            (car.top_speed / 200) * 20 +            # Top speed normalized to ~100
            (car.handling / 10) * 15 +              # Handling score out of 10
            year_factor * 5                         # Small bonus for newer cars
        )
        
        logger.info(f"Performance score for {car.make} {car.model}: {performance:.3f}")
        return performance

    def clear_cache(self):
        """Clears the local TTL cache of car objects.
        """
        logger.info("Clearing local car cache in TrackModel.")
        self._car_cache.clear()
        self._ttl.clear()
        logger.info("Car cache cleared successfully.") 
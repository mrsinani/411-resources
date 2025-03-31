import logging
import math
from typing import List

from boxing.models.boxers_model import Boxer, update_boxer_stats
from boxing.utils.logger import configure_logger
from boxing.utils.api_utils import get_random


logger = logging.getLogger(__name__)
configure_logger(logger)


class RingModel:
    """Represents a ring where two Boxer objects can fight.

    Attributes:
        ring (List[Boxer]): A list that can contain two boxers that will be fighting.
    """

    def __init__(self) -> None:
        """Initalizes an empty Ring."""
        self.ring: List[Boxer] = []
        logger.info("Ring initialized")

    def fight(self) -> str:
        """Simulates a fight between the two boxers in the ring.

        Returns:
            winner.name: The name of the winning boxer.

        Raises:
            ValueError: If there are not exactly 2 fighters within the ring.
        """
        logger.info("Starting fight simulation")
        
        if len(self.ring) < 2:
            logger.error("Cannot start fight: not enough boxers in the ring")
            raise ValueError("There must be two boxers to start a fight.")

        boxer_1, boxer_2 = self.get_boxers()
        logger.info(f"Fighters in the ring: {boxer_1.name} vs {boxer_2.name}")

        skill_1 = self.get_fighting_skill(boxer_1)
        skill_2 = self.get_fighting_skill(boxer_2)
        logger.debug(f"Fighting skills: {boxer_1.name}={skill_1}, {boxer_2.name}={skill_2}")

        # Compute the absolute skill difference
        # And normalize using a logistic function for better probability scaling
        delta = abs(skill_1 - skill_2)
        normalized_delta = 1 / (1 + math.e ** (-delta))

        random_number = get_random()
        logger.debug(f"Random number for fight determination: {random_number}")

        if random_number < normalized_delta:
            winner = boxer_1
            loser = boxer_2
        else:
            winner = boxer_2
            loser = boxer_1

        logger.info(f"Fight result: {winner.name} defeats {loser.name}")
        update_boxer_stats(winner.id, "win")
        update_boxer_stats(loser.id, "loss")

        self.clear_ring()
        logger.info("Ring cleared after fight")

        return winner.name

    def clear_ring(self) -> None:
        """Clears out the Boxer objects stored within the ring."""
        logger.info("Clearing the ring")
        if not self.ring:
            logger.info("Ring is already empty")
            return
        self.ring.clear()
        logger.info("Ring has been cleared")

    def enter_ring(self, boxer: Boxer) -> None:
        """Inserts a boxer into the ring if there is space.

        Args:
            boxer: An Boxer object that will be entered into the ring if possible.

        Raises:
            TypeError: If input is not a single instance of a Boxer or a tuple of Boxers.
            ValueError: If input fills ring with more than 2 Boxer objects within the ring at the same time.
        """
        logger.info(f"Attempting to enter boxer {boxer.name} into the ring")
        
        if not isinstance(boxer, Boxer):
            logger.error(f"Invalid type: Expected 'Boxer', got '{type(boxer).__name__}'")
            raise TypeError(
                f"Invalid type: Expected 'Boxer', got '{type(boxer).__name__}'"
            )

        if len(self.ring) >= 2:
            logger.warning("Ring is full, cannot add more boxers")
            raise ValueError("Ring is full, cannot add more boxers.")

        self.ring.append(boxer)
        logger.info(f"Boxer {boxer.name} has entered the ring (ring size: {len(self.ring)})")

    def get_boxers(self) -> List[Boxer]:
        """Return the boxers that are in the ring, if a ring exists.

        Returns:
            self.ring: Returns a list of Boxer(s) within the ring.
        """
        logger.info(f"Retrieving boxers from the ring (count: {len(self.ring)})")
        if not self.ring:
            logger.warning("Ring is empty")
        else:
            boxer_names = [boxer.name for boxer in self.ring]
            logger.info(f"Boxers in ring: {', '.join(boxer_names)}")

        return self.ring

    def get_fighting_skill(self, boxer: Boxer) -> float:
        """Return the fighting skill of a boxer based on a formula.

        Args:
            boxer: A Boxer object whose skill will be calculated.

        Returns:
            skill: A value calculated through the weight of a boxer, their name, their reach, and age.
        """
        logger.debug(f"Calculating fighting skill for boxer: {boxer.name}")
        
        # Arbitrary calculations
        age_modifier = -1 if boxer.age < 25 else (-2 if boxer.age > 35 else 0)
        skill = (boxer.weight * len(boxer.name)) + (boxer.reach / 10) + age_modifier

        logger.debug(f"Calculated skill for {boxer.name}: {skill}")
        return skill

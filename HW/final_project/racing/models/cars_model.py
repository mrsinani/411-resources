import logging
from typing import List

from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from racing.db import db
from racing.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


class Cars(db.Model):
    """Represents a racing car in the system.

    This model maps to the 'cars' table in the database and stores vehicle
    attributes such as make, model, horsepower, weight, acceleration, top_speed,
    handling, and race statistics. Used in a Flask-SQLAlchemy application to
    manage car data, run simulations, and track race outcomes.
    """

    __tablename__ = 'cars'
    
    id = db.Column(db.Integer, primary_key=True)
    make = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    horsepower = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)  # In pounds
    zero_to_sixty = db.Column(db.Float, nullable=False)  # 0-60 mph time in seconds
    top_speed = db.Column(db.Integer, nullable=False)  # In mph
    handling = db.Column(db.Integer, nullable=False)  # 1-10 rating
    car_class = db.Column(db.String(50), nullable=False)
    races = db.Column(db.Integer, default=0)
    wins = db.Column(db.Integer, default=0)

    def __init__(self, make: str, model: str, year: int, horsepower: int, 
                 weight: float, zero_to_sixty: float, top_speed: int, handling: int):
        """Initialize a new Car instance with basic attributes.

        Args:
            make (str): The car's manufacturer
            model (str): The car's model name
            year (int): The car's model year. Must be between 1950 and current year.
            horsepower (int): The engine horsepower. Must be greater than 0.
            weight (float): The car's weight in pounds. Must be greater than 0.
            zero_to_sixty (float): 0-60 mph acceleration time in seconds. Must be greater than 0.
            top_speed (int): Maximum speed in mph. Must be greater than 0.
            handling (int): Handling rating from 1-10. Must be between 1 and 10.

        Notes:
            - The car's class is automatically assigned based on horsepower to weight ratio.
            - Race statistics (`races` and `wins`) are initialized to 0 by default.
        """
        self.make = make
        self.model = model
        self.year = year
        self.horsepower = horsepower
        self.weight = weight
        self.zero_to_sixty = zero_to_sixty
        self.top_speed = top_speed
        self.handling = handling
        self.car_class = self.get_car_class(horsepower, weight)
        self.races = 0
        self.wins = 0

    @classmethod
    def get_car_class(cls, horsepower: int, weight: float) -> str:
        """Determine the car class based on power-to-weight ratio.

        Args:
            horsepower: The horsepower of the car.
            weight: The weight of the car in pounds.

        Returns:
            str: The car class: Economy, Sport, Super, Hyper.

        Raises:
            ValueError: If horsepower or weight are not positive values.
        """
        if horsepower <= 0:
            raise ValueError("Horsepower must be greater than 0.")
        if weight <= 0:
            raise ValueError("Weight must be greater than 0.")

        power_to_weight = horsepower / weight * 1000  # Power to weight ratio in hp per 1000 pounds

        if power_to_weight < 100:
            return "Economy"
        elif power_to_weight < 200:
            return "Sport"
        elif power_to_weight < 300:
            return "Super"
        else:
            return "Hyper"

    @classmethod
    def create_car(cls, make: str, model: str, year: int, horsepower: int,
                   weight: float, zero_to_sixty: float, top_speed: int, handling: int) -> None:
        """Create and persist a new Car instance.

        Args:
            make: The make of the car.
            model: The model of the car.
            year: The year of the car.
            horsepower: The horsepower of the car.
            weight: The weight of the car in pounds.
            zero_to_sixty: The 0-60 mph acceleration time in seconds.
            top_speed: The top speed of the car in mph.
            handling: The handling rating of the car (1-10).

        Raises:
            IntegrityError: If a car with the same make and model already exists.
            ValueError: If any of the input parameters are invalid.
            SQLAlchemyError: If there is a database error during creation.
        """
        logger.info(f"Creating car: {make} {model}, {year=} {horsepower=} {weight=} {zero_to_sixty=} {top_speed=} {handling=}")

        # Validate inputs
        if not make or not model:
            logger.error("Make and model must not be empty.")
            raise ValueError("Make and model must not be empty.")
            
        if year < 1950 or year > 2025:  # Adjust upper limit as needed
            logger.error(f"Invalid year: {year}. Year must be between 1950 and 2025.")
            raise ValueError(f"Invalid year: {year}. Year must be between 1950 and 2025.")
            
        if horsepower <= 0:
            logger.error(f"Invalid horsepower: {horsepower}. Must be greater than 0.")
            raise ValueError(f"Invalid horsepower: {horsepower}. Must be greater than 0.")
            
        if weight <= 0:
            logger.error(f"Invalid weight: {weight}. Must be greater than 0.")
            raise ValueError(f"Invalid weight: {weight}. Must be greater than 0.")
            
        if zero_to_sixty <= 0:
            logger.error(f"Invalid 0-60 time: {zero_to_sixty}. Must be greater than 0.")
            raise ValueError(f"Invalid 0-60 time: {zero_to_sixty}. Must be greater than 0.")
            
        if top_speed <= 0:
            logger.error(f"Invalid top speed: {top_speed}. Must be greater than 0.")
            raise ValueError(f"Invalid top speed: {top_speed}. Must be greater than 0.")
            
        if handling < 1 or handling > 10:
            logger.error(f"Invalid handling: {handling}. Must be between 1 and 10.")
            raise ValueError(f"Invalid handling: {handling}. Must be between 1 and 10.")

        try:
            car = cls(make, model, year, horsepower, weight, zero_to_sixty, top_speed, handling)
            db.session.add(car)
            db.session.commit()
            logger.info(f"Car created successfully: {make} {model}")
        except IntegrityError:
            db.session.rollback()
            logger.error(f"Car with make '{make}' and model '{model}' already exists.")
            raise ValueError(f"Car with make '{make}' and model '{model}' already exists.")
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(f"Database error during creation: {e}")
            raise

    @classmethod
    def get_car_by_id(cls, car_id: int) -> "Cars":
        """Retrieve a car by ID.

        Args:
            car_id: The ID of the car.

        Returns:
            Cars: The car instance.

        Raises:
            ValueError: If the car with the given ID does not exist.
        """
        car = cls.query.get(car_id)
        if car is None:
            logger.info(f"Car with ID {car_id} not found.")
            raise ValueError(f"Car with ID {car_id} not found.")
        return car

    @classmethod
    def get_car_by_make_model(cls, make: str, model: str) -> "Cars":
        """Retrieve a car by make and model.

        Args:
            make: The make of the car.
            model: The model of the car.

        Returns:
            Cars: The car instance.

        Raises:
            ValueError: If the car with the given make and model does not exist.
        """
        car = cls.query.filter_by(make=make, model=model).first()
        if car is None:
            logger.info(f"Car '{make} {model}' not found.")
            raise ValueError(f"Car '{make} {model}' not found.")
        return car

    @classmethod
    def delete(cls, car_id: int) -> None:
        """Delete a car by ID.

        Args:
            car_id: The ID of the car to delete.

        Raises:
            ValueError: If the car with the given ID does not exist.
        """
        car = cls.get_car_by_id(car_id)
        db.session.delete(car)
        db.session.commit()
        logger.info(f"Car with ID {car_id} permanently deleted.")

    def update_stats(self, result: str) -> None:
        """Update the car's race and win count based on result.

        Args:
            result: The result of the race ('win' or 'loss').

        Raises:
            ValueError: If the result is not 'win' or 'loss'.
            ValueError: If the number of wins exceeds the number of races.
        """
        if result not in {"win", "loss"}:
            raise ValueError("Result must be 'win' or 'loss'.")

        self.races += 1
        if result == "win":
            self.wins += 1

        if self.wins > self.races:
            raise ValueError("Wins cannot exceed number of races.")

        db.session.commit()
        logger.info(f"Updated stats for car {self.make} {self.model}: {self.races} races, {self.wins} wins.")

    @staticmethod
    def get_leaderboard(sort_by: str = "wins") -> List[dict]:
        """Retrieve a sorted leaderboard of cars.

        Args:
            sort_by (str): Either "wins" or "win_pct".

        Returns:
            List[Dict]: List of cars with stats and win percentage.

        Raises:
            ValueError: If the sort_by parameter is not valid.
        """
        logger.info(f"Retrieving leaderboard. Sort by: {sort_by}")

        if sort_by not in {"wins", "win_pct"}:
            logger.error(f"Invalid sort_by parameter: {sort_by}")
            raise ValueError(f"Invalid sort_by parameter: {sort_by}")

        cars = Cars.query.filter(Cars.races > 0).all()

        def compute_win_pct(c: Cars) -> float:
            return round((c.wins / c.races) * 100, 1) if c.races > 0 else 0.0

        leaderboard = [{
            "id": c.id,
            "make": c.make,
            "model": c.model,
            "year": c.year,
            "horsepower": c.horsepower,
            "weight": c.weight,
            "zero_to_sixty": c.zero_to_sixty,
            "top_speed": c.top_speed,
            "handling": c.handling,
            "car_class": c.car_class,
            "races": c.races,
            "wins": c.wins,
            "win_pct": compute_win_pct(c)
        } for c in cars]

        leaderboard.sort(key=lambda c: c[sort_by], reverse=True)
        logger.info("Leaderboard retrieved successfully.")
        return leaderboard 
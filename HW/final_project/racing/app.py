from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, Response, request
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS

from config import ProductionConfig

from racing.db import db
from racing.models.cars_model import Cars
from racing.models.track_model import TrackModel
from racing.models.user_model import Users
from racing.utils.logger import configure_logger


load_dotenv()

def create_app(config_class=ProductionConfig):
    app = Flask(__name__)
    CORS(app, supports_credentials=True, origins=["http://localhost:3000"])
    configure_logger(app.logger)

    app.config.from_object(config_class)

    db.init_app(app)  # Initialize db with app
    with app.app_context():
        db.create_all()  # Recreate all tables

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.filter_by(username=user_id).first()

    @login_manager.unauthorized_handler
    def unauthorized():
        return make_response(jsonify({
            "status": "error",
            "message": "Authentication required"
        }), 401)


    track_model = TrackModel()


    ####################################################
    #
    # Healthchecks
    #
    ####################################################


    @app.route('/api/health', methods=['GET'])
    def healthcheck() -> Response:
        """
        Health check route to verify the service is running.

        Returns:
            JSON response indicating the health status of the service.
        """
        app.logger.info("Health check endpoint hit")
        return make_response(jsonify({
            'status': 'success',
            'message': 'Service is running'
        }), 200)


    ##########################################################
    #
    # User Management
    #
    #########################################################

    @app.route('/api/create-user', methods=['PUT'])
    def create_user() -> Response:
        """Register a new user account.

        Expected JSON Input:
            - username (str): The desired username.
            - password (str): The desired password.

        Returns:
            JSON response indicating the success of the user creation.

        Raises:
            400 error if the username or password is missing.
            500 error if there is an issue creating the user in the database.
        """
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Username and password are required"
                }), 400)

            Users.create_user(username, password)
            return make_response(jsonify({
                "status": "success",
                "message": f"User '{username}' created successfully"
            }), 201)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"User creation failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while creating user",
                "details": str(e)
            }), 500)

    @app.route('/api/login', methods=['POST'])
    def login() -> Response:
        """Authenticate a user and log them in.

        Expected JSON Input:
            - username (str): The username of the user.
            - password (str): The password of the user.

        Returns:
            JSON response indicating the success of the login attempt.

        Raises:
            401 error if the username or password is incorrect.
        """
        try:
            data = request.get_json()
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Username and password are required"
                }), 400)

            if Users.check_password(username, password):
                user = Users.query.filter_by(username=username).first()
                login_user(user)
                return make_response(jsonify({
                    "status": "success",
                    "message": f"User '{username}' logged in successfully"
                }), 200)
            else:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid username or password"
                }), 401)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 401)
        except Exception as e:
            app.logger.error(f"Login failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred during login",
                "details": str(e)
            }), 500)

    @app.route('/api/logout', methods=['POST'])
    @login_required
    def logout() -> Response:
        """Log out the current user.

        Returns:
            JSON response indicating the success of the logout operation.
        """
        logout_user()
        return make_response(jsonify({
            "status": "success",
            "message": "User logged out successfully"
        }), 200)

    @app.route('/api/change-password', methods=['POST'])
    @login_required
    def change_password() -> Response:
        """Change the password for the current user.

        Expected JSON Input:
            - new_password (str): The new password to set.

        Returns:
            JSON response indicating the success of the password change.

        Raises:
            400 error if the new password is not provided.
            500 error if there is an issue updating the password in the database.
        """
        try:
            data = request.get_json()
            new_password = data.get("new_password")

            if not new_password:
                return make_response(jsonify({
                    "status": "error",
                    "message": "New password is required"
                }), 400)

            username = current_user.username
            Users.update_password(username, new_password)
            return make_response(jsonify({
                "status": "success",
                "message": "Password changed successfully"
            }), 200)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Password change failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while changing password",
                "details": str(e)
            }), 500)

    @app.route('/api/reset-users', methods=['DELETE'])
    def reset_users() -> Response:
        """Recreate the users table to delete all users.

        Returns:
            JSON response indicating the success of recreating the Users table.

        Raises:
            500 error if there is an issue recreating the Users table.
        """
        try:
            app.logger.info("Received request to recreate Users table")
            with app.app_context():
                Users.__table__.drop(db.engine)
                Users.__table__.create(db.engine)
            app.logger.info("Users table recreated successfully")
            return make_response(jsonify({
                "status": "success",
                "message": f"Users table recreated successfully"
            }), 200)
        except Exception as e:
            app.logger.error(f"Failed to recreate Users table: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while recreating Users table",
                "details": str(e)
            }), 500)


    ##########################################################
    #
    # Car Management
    #
    #########################################################

    @app.route('/api/reset-cars', methods=['DELETE'])
    def reset_cars() -> Response:
        """Recreate the cars table to delete all cars.

        Returns:
            JSON response indicating the success of recreating the Cars table.

        Raises:
            500 error if there is an issue recreating the Cars table.
        """
        try:
            app.logger.info("Received request to recreate Cars table")
            with app.app_context():
                Cars.__table__.drop(db.engine)
                Cars.__table__.create(db.engine)
            app.logger.info("Cars table recreated successfully")
            return make_response(jsonify({
                "status": "success",
                "message": f"Cars table recreated successfully"
            }), 200)
        except Exception as e:
            app.logger.error(f"Failed to recreate Cars table: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while recreating Cars table",
                "details": str(e)
            }), 500)

    @app.route('/api/add-car', methods=['POST'])
    @login_required
    def add_car() -> Response:
        """Add a new car to the system.

        Expected JSON Input:
            - make (str): The make of the car.
            - model (str): The model of the car.
            - year (int): The year of the car.
            - horsepower (int): The horsepower of the car.
            - weight (float): The weight of the car in pounds.
            - zero_to_sixty (float): 0-60 mph time in seconds.
            - top_speed (int): The top speed of the car in mph.
            - handling (int): Handling rating from 1-10.

        Returns:
            JSON response indicating the success of the car creation.

        Raises:
            400 error if any required field is missing or invalid.
            500 error if there is an issue creating the car in the database.
        """
        try:
            data = request.get_json()
            make = data.get("make")
            model = data.get("model")
            year = data.get("year")
            horsepower = data.get("horsepower")
            weight = data.get("weight")
            zero_to_sixty = data.get("zero_to_sixty")
            top_speed = data.get("top_speed")
            handling = data.get("handling")

            # Validate required fields
            if not all([make, model, year, horsepower, weight, zero_to_sixty, top_speed, handling]):
                return make_response(jsonify({
                    "status": "error",
                    "message": "All car attributes are required"
                }), 400)

            # Convert numeric values
            try:
                year = int(year)
                horsepower = int(horsepower)
                weight = float(weight)
                zero_to_sixty = float(zero_to_sixty)
                top_speed = int(top_speed)
                handling = int(handling)
            except ValueError:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Invalid numeric values provided"
                }), 400)

            Cars.create_car(make, model, year, horsepower, weight, zero_to_sixty, top_speed, handling)
            
            return make_response(jsonify({
                "status": "success",
                "message": f"Car '{make} {model}' added successfully",
                "car_class": Cars.get_car_class(horsepower, weight)
            }), 201)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Failed to add car: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while adding car",
                "details": str(e)
            }), 500)

    @app.route('/api/delete-car/<int:car_id>', methods=['DELETE'])
    @login_required
    def delete_car(car_id: int) -> Response:
        """Delete a car from the system.

        Args:
            car_id: The ID of the car to delete.

        Returns:
            JSON response indicating the success of the car deletion.

        Raises:
            404 error if the car does not exist.
            500 error if there is an issue deleting the car from the database.
        """
        try:
            car = Cars.get_car_by_id(car_id)
            car_name = f"{car.make} {car.model}"
            
            Cars.delete(car_id)
            
            return make_response(jsonify({
                "status": "success",
                "message": f"Car '{car_name}' deleted successfully"
            }), 200)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 404)
        except Exception as e:
            app.logger.error(f"Failed to delete car: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while deleting car",
                "details": str(e)
            }), 500)

    @app.route('/api/get-car-by-id/<int:car_id>', methods=['GET'])
    @login_required
    def get_car_by_id(car_id: int) -> Response:
        """Get a car by its ID.

        Args:
            car_id: The ID of the car to retrieve.

        Returns:
            JSON response containing the car details.

        Raises:
            404 error if the car does not exist.
            500 error if there is an issue retrieving the car from the database.
        """
        try:
            car = Cars.get_car_by_id(car_id)
            
            return make_response(jsonify({
                "status": "success",
                "car": {
                    "id": car.id,
                    "make": car.make,
                    "model": car.model,
                    "year": car.year,
                    "horsepower": car.horsepower,
                    "weight": car.weight,
                    "zero_to_sixty": car.zero_to_sixty,
                    "top_speed": car.top_speed,
                    "handling": car.handling,
                    "car_class": car.car_class,
                    "races": car.races,
                    "wins": car.wins
                }
            }), 200)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 404)
        except Exception as e:
            app.logger.error(f"Failed to retrieve car: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while retrieving car",
                "details": str(e)
            }), 500)

    @app.route('/api/get-car-by-make-model/<string:make>/<string:model>', methods=['GET'])
    @login_required
    def get_car_by_make_model(make: str, model: str) -> Response:
        """Get a car by its make and model.

        Args:
            make: The make of the car to retrieve.
            model: The model of the car to retrieve.

        Returns:
            JSON response containing the car details.

        Raises:
            404 error if the car does not exist.
            500 error if there is an issue retrieving the car from the database.
        """
        try:
            car = Cars.get_car_by_make_model(make, model)
            
            return make_response(jsonify({
                "status": "success",
                "car": {
                    "id": car.id,
                    "make": car.make,
                    "model": car.model,
                    "year": car.year,
                    "horsepower": car.horsepower,
                    "weight": car.weight,
                    "zero_to_sixty": car.zero_to_sixty,
                    "top_speed": car.top_speed,
                    "handling": car.handling,
                    "car_class": car.car_class,
                    "races": car.races,
                    "wins": car.wins
                }
            }), 200)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 404)
        except Exception as e:
            app.logger.error(f"Failed to retrieve car: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while retrieving car",
                "details": str(e)
            }), 500)

    @app.route('/api/race', methods=['GET'])
    @login_required
    def race() -> Response:
        """Start a race between two cars on the track.

        Returns:
            JSON response indicating the winner of the race.

        Raises:
            400 error if there are not enough cars on the track.
            500 error if there is an issue during the race.
        """
        try:
            winner = track_model.race()
            
            return make_response(jsonify({
                "status": "success",
                "message": f"Race completed successfully",
                "winner": winner
            }), 200)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except RuntimeError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 500)
        except Exception as e:
            app.logger.error(f"Race failed: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred during the race",
                "details": str(e)
            }), 500)

    @app.route('/api/clear-track', methods=['POST'])
    @login_required
    def clear_track() -> Response:
        """Clear all cars from the track.

        Returns:
            JSON response indicating the success of clearing the track.

        Raises:
            500 error if there is an issue clearing the track.
        """
        try:
            track_model.clear_track()
            return make_response(jsonify({
                "status": "success",
                "message": "Track cleared successfully"
            }), 200)
        except Exception as e:
            app.logger.error(f"Failed to clear track: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while clearing track",
                "details": str(e)
            }), 500)

    @app.route('/api/enter-track', methods=['POST'])
    @login_required
    def enter_track() -> Response:
        """Add a car to the track for an upcoming race.

        Expected JSON Input:
            - car_id (int): The ID of the car to add to the track.

        Returns:
            JSON response indicating the success of adding the car to the track.

        Raises:
            400 error if the car_id is missing or invalid.
            404 error if the car does not exist.
            500 error if there is an issue adding the car to the track.
        """
        try:
            data = request.get_json()
            car_id = data.get("car_id")

            if car_id is None:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Car ID is required"
                }), 400)

            try:
                car_id = int(car_id)
            except ValueError:
                return make_response(jsonify({
                    "status": "error",
                    "message": "Car ID must be an integer"
                }), 400)

            track_model.enter_track(car_id)
            
            # Get car details for response
            car = Cars.get_car_by_id(car_id)
            
            return make_response(jsonify({
                "status": "success",
                "message": f"{car.make} {car.model} entered the track",
                "cars_on_track": len(track_model.track)
            }), 200)

        except ValueError as e:
            # This could be a "track is full" error or "car not found" error
            if "not found" in str(e).lower():
                return make_response(jsonify({
                    "status": "error",
                    "message": str(e)
                }), 404)
            else:
                return make_response(jsonify({
                    "status": "error",
                    "message": str(e)
                }), 400)
        except Exception as e:
            app.logger.error(f"Failed to add car to track: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while adding car to track",
                "details": str(e)
            }), 500)

    @app.route('/api/get-cars', methods=['GET'])
    @login_required
    def get_cars() -> Response:
        """Get all cars in the system.

        Returns:
            JSON response containing a list of all cars.

        Raises:
            500 error if there is an issue retrieving cars from the database.
        """
        try:
            cars = Cars.query.all()
            
            car_list = [{
                "id": car.id,
                "make": car.make,
                "model": car.model,
                "year": car.year,
                "horsepower": car.horsepower,
                "weight": car.weight,
                "zero_to_sixty": car.zero_to_sixty,
                "top_speed": car.top_speed,
                "handling": car.handling,
                "car_class": car.car_class,
                "races": car.races,
                "wins": car.wins
            } for car in cars]
            
            return make_response(jsonify({
                "status": "success",
                "count": len(car_list),
                "cars": car_list
            }), 200)

        except Exception as e:
            app.logger.error(f"Failed to retrieve cars: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while retrieving cars",
                "details": str(e)
            }), 500)

    @app.route('/api/leaderboard', methods=['GET'])
    def get_leaderboard() -> Response:
        """Get the leaderboard of cars ranked by wins or win percentage.

        Query Parameters:
            - sort_by (str): The field to sort by - "wins" or "win_pct". Default: "wins".

        Returns:
            JSON response containing the leaderboard.

        Raises:
            400 error if the sort_by parameter is invalid.
            500 error if there is an issue retrieving the leaderboard.
        """
        try:
            sort_by = request.args.get("sort_by", "wins")
            
            if sort_by not in ["wins", "win_pct"]:
                return make_response(jsonify({
                    "status": "error",
                    "message": f"Invalid sort_by parameter: {sort_by}. Must be 'wins' or 'win_pct'."
                }), 400)
            
            leaderboard = Cars.get_leaderboard(sort_by)
            
            return make_response(jsonify({
                "status": "success",
                "count": len(leaderboard),
                "sort_by": sort_by,
                "leaderboard": leaderboard
            }), 200)

        except ValueError as e:
            return make_response(jsonify({
                "status": "error",
                "message": str(e)
            }), 400)
        except Exception as e:
            app.logger.error(f"Failed to retrieve leaderboard: {e}")
            return make_response(jsonify({
                "status": "error",
                "message": "An internal error occurred while retrieving leaderboard",
                "details": str(e)
            }), 500)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True) 
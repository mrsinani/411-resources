# Car Racing Application

A Flask-based API for managing cars and simulating races between them.

## Features

- Car management with detailed attributes (make, model, year, horsepower, weight, 0-60 time, top speed, handling)
- Car classification based on power-to-weight ratio
- Race simulation between two cars with performance calculations
- User authentication system
- Leaderboard tracking of race statistics
- Local TTL caching of car data

## Setup and Installation

### Using Docker

The easiest way to run the application is using Docker:

1. Make sure Docker is installed on your system
2. Clone this repository
3. Run the Docker script:

```bash
chmod +x run_docker.sh
./run_docker.sh
```

The application will be available at `http://localhost:5000`.

### Local Development

To set up for local development:

1. Clone this repository
2. Set up a virtual environment:

```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

3. Activate the virtual environment:

```bash
source .venv/bin/activate
```

4. Run the application:

```bash
python app.py
```

## API Endpoints

### Authentication

- `PUT /api/create-user` - Create a new user
- `POST /api/login` - Log in as a user
- `POST /api/logout` - Log out
- `POST /api/change-password` - Change user password

### Car Management

- `POST /api/add-car` - Add a new car
- `GET /api/get-cars` - Get all cars
- `GET /api/get-car-by-id/<car_id>` - Get a car by ID
- `GET /api/get-car-by-make-model/<make>/<model>` - Get a car by make and model
- `DELETE /api/delete-car/<car_id>` - Delete a car

### Racing

- `POST /api/enter-track` - Add a car to the track for a race
- `GET /api/race` - Simulate a race between two cars
- `POST /api/clear-track` - Clear all cars from the track
- `GET /api/leaderboard` - Get the racing leaderboard

### System

- `GET /api/health` - Health check
- `DELETE /api/reset-users` - Reset users table
- `DELETE /api/reset-cars` - Reset cars table

## Sample Car Data

Below are some example cars to add to the system:

### Sports Cars

```json
{
  "make": "Porsche",
  "model": "911 Carrera",
  "year": 2022,
  "horsepower": 379,
  "weight": 3354,
  "zero_to_sixty": 4.0,
  "top_speed": 182,
  "handling": 9
}
```

```json
{
  "make": "Chevrolet",
  "model": "Corvette C8",
  "year": 2023,
  "horsepower": 495,
  "weight": 3647,
  "zero_to_sixty": 2.9,
  "top_speed": 194,
  "handling": 8
}
```

### Supercars

```json
{
  "make": "Ferrari",
  "model": "F8 Tributo",
  "year": 2021,
  "horsepower": 710,
  "weight": 3164,
  "zero_to_sixty": 2.8,
  "top_speed": 211,
  "handling": 9
}
```

```json
{
  "make": "Lamborghini",
  "model": "Huracan Evo",
  "year": 2022,
  "horsepower": 640,
  "weight": 3135,
  "zero_to_sixty": 2.9,
  "top_speed": 202,
  "handling": 9
}
```

### Economy Cars

```json
{
  "make": "Honda",
  "model": "Civic",
  "year": 2023,
  "horsepower": 158,
  "weight": 2877,
  "zero_to_sixty": 7.9,
  "top_speed": 137,
  "handling": 6
}
```

```json
{
  "make": "Toyota",
  "model": "Corolla",
  "year": 2023,
  "horsepower": 169,
  "weight": 3110,
  "zero_to_sixty": 8.2,
  "top_speed": 118,
  "handling": 5
}
```

## License

This project is licensed under the MIT License.

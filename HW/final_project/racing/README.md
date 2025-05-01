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

# API Route Documentation

---

### **Route: `/api/create-user`**
- **Request Type:** PUT  
- **Purpose:** Registers a new user account.  
- **Request Body:**  
  - `username` (String): Desired username  
  - `password` (String): Desired password  
- **Response Format:** JSON 
  - `status` (String): response status - success or error
  - `message` (String): status description 
  - **Success Response Example:**  
    - Code: 201  
    - Content: `{ "status": "success", "message": "User 'example' created successfully" }`  
      
- **Example Request:**
```json
{
  "username": "newuser",
  "password": "securepass123"
}
```
- **Example Response:**
```json
{
  "status": "success",
  "message": "User 'newuser' created successfully"
}
```

---

### **Route: `/api/login`**
- **Request Type:** POST  
- **Purpose:** Authenticates and logs in a user.  
- **Request Body:**  
  - `username` (String): User's username  
  - `password` (String): User's password  
- **Response Format:** JSON  
  - `status` (String): response status - success or error
  - `message` (String): status description 
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "message": "User 'newuser' logged in successfully" }` 
- **Example Request:**
```json
{
  "username": "newuser",
  "password": "securepass123"
}
```
- **Example Response:**
```json
{
  "status": "success",
  "message": "User 'newuser' logged in successfully"
}
```

---

### **Route: `/api/logout`**
- **Request Type:** POST  
- **Purpose:** Logs out the current user.  
- **Request Body:** None  
- **Response Format:** JSON 
  - `status` (String): response status - success or error
  - `message` (String): status description 
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "message": "User logged out successfully" }` 

- **Example Response:**
```json
{
  "status": "success",
  "message": "User logged out successfully"
}
```

---

### **Route: `/api/change-password`**
- **Request Type:** POST  
- **Purpose:** Changes the password for the current user.  
- **Request Body:**  
  - `new_password` (String): New password to be set  
- **Response Format:** JSON
  - `status` (String): response status - success or error
  - `message` (String): status description   
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "message": "Password changed successfully" }`  

- **Example Request:**
```json
{
  "new_password": "newsecurepassword"
}
```
- **Example Response:**
```json
{
  "status": "success",
  "message": "Password changed successfully"
}
```

---

### **Route: `/api/reset-users`**
- **Request Type:** DELETE  
- **Purpose:** Deletes all users by recreating the Users table.  
- **Request Body:** None  
- **Response Format:** JSON
  - `status` (String): response status - success or error
  - `message` (String): status description   
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "message": "Users table recreated successfully" }` 

- **Example Response:**
```json
{
  "status": "success",
  "message": "Users table recreated successfully"
}
```

---

### **Route: `/api/add-car`**
- **Request Type:** POST  
- **Purpose:** Adds a new car to the system.  
- **Request Body:**  
  - `make` (String): car manufacturer
  - `model` (String): car model
  - `year` (Integer): year the car was produced
  - `horsepower` (Integer): horsepower of the car
  - `weight` (Float): weight of the car in pounds
  - `zero_to_sixty` (Float): 0-60 mph time in seconds
  - `top_speed` (Integer): top speed of car in miles per hour
  - `handling` (Integer): handling rating from 1-10  
- **Response Format:** JSON 
  - `status` (String): response status - success or error
  - `message` (String): status description
  - `car_class` (String): class of car added 
  - **Success Response Example:**  
    - Code: 201  
    - Content: `{ "status": "success", "message": "Car 'Toyota Supra' added successfully", "car_class": "Economy" }` 
      
- **Example Request:**
```json
{
  "make": "Toyota",
  "model": "Supra",
  "year": 2020,
  "horsepower": 335,
  "weight": 3450.5,
  "zero_to_sixty": 4.1,
  "top_speed": 155,
  "handling": 8
}
```
- **Example Response:**
```json
{
  "status": "success",
  "message": "Car 'Toyota Supra' added successfully",
  "car_class": "Economy"
}
```

---

### **Route: `/api/delete-car/<car_id>`**
- **Request Type:** DELETE  
- **Purpose:** Deletes a car by its ID.  
- **Path Parameter:**  
  - `car_id` (Integer): Car's ID  
- **Response Format:** JSON 
  - `status` (String): response status - success or error
  - `message` (String): status description
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "message": "Car 'Toyota Supra' deleted successfully" }`
- **Example Request:**
```bash
curl -X DELETE http://localhost:5000/api/delete-car/1

```
- **Example Response:**
```json
{
  "status": "success",
  "message": "Car 'Toyota Supra' deleted successfully"
}
```   

---

### **Route: `/api/get-car-by-id/<car_id>`**
- **Request Type:** GET  
- **Purpose:** Retrieves car details by ID.  
- **Path Parameter:**  
  - `car_id` (Integer): Car's ID  
- **Response Format:** JSON 
  - `status` (String): response status - success or error
  - `car` (Car object): car characteristics
    - `id`: unique identifier for car
    - `make` (String): car manufacturer
    - `model` (String): car model
    - `year` (Integer): year the car was produced
    - `horsepower` (Integer): horsepower of the car
    - `weight` (Float): weight of the car in pounds
    - `zero_to_sixty` (Float): 0-60 mph time in seconds
    - `top_speed` (Integer): top speed of car in miles per hour
    - `handling` (Integer): handling rating from 1-10
    - `car_class` (String): class of car
    - `races` (Integer): number of races participated in
    - `wins` (Integer): number of races won
  - **Success Response Example:**  
    - Code: 200  
    - Content: 
    ```json
    {
        "status": "success",
        "car": {
            "id": 1,
            "make": "Toyota",
            "model": "Supra",
            "year": 2020,
            "horsepower": 335,
            "weight": 3450.5,
            "zero_to_sixty": 4.1,
            "top_speed": 155,
            "handling": 8,
            "car_class": "Economy",
            "races": 2,
            "wins": 1
        }
    }
    ```
- **Example Request:**
```bash
curl -X GET http://localhost:5000/api/get-car-by-id/1
```
- **Example Response:**
```json
    {
        "status": "success",
        "car": {
            "id": 1,
            "make": "Toyota",
            "model": "Supra",
            "year": 2020,
            "horsepower": 335,
            "weight": 3450.5,
            "zero_to_sixty": 4.1,
            "top_speed": 155,
            "handling": 8,
            "car_class": "Economy",
            "races": 2,
            "wins": 1
        }
    }
```

---

### **Route: `/api/get-car-by-make-model/<make>/<model>`**
- **Request Type:** GET  
- **Purpose:** Retrieves car details by make and model.  
- **Path Parameters:**  
  - `make` (String): Car make  
  - `model` (String): Car model  
- **Response Format:** JSON  
  - `status` (String): response status - success or error
  - `car` (Car object): car characteristics
    - `id`: unique identifier for car
    - `make` (String): car manufacturer
    - `model` (String): car model
    - `year` (Integer): year the car was produced
    - `horsepower` (Integer): horsepower of the car
    - `weight` (Float): weight of the car in pounds
    - `zero_to_sixty` (Float): 0-60 mph time in seconds
    - `top_speed` (Integer): top speed of car in miles per hour
    - `handling` (Integer): handling rating from 1-10
    - `car_class` (String): class of car
    - `races` (Integer): number of races participated in
    - `wins` (Integer): number of races won
  - **Success Response Example:**  
    - Code: 200  
    - Content: 
    ```json
    {
        "status": "success",
        "car": {
            "id": 1,
            "make": "Toyota",
            "model": "Supra",
            "year": 2020,
            "horsepower": 335,
            "weight": 3450.5,
            "zero_to_sixty": 4.1,
            "top_speed": 155,
            "handling": 8,
            "car_class": "Economy",
            "races": 2,
            "wins": 1
        }
    }
    ```
- **Example Request:**
```bash
curl -X GET http://localhost:5000/api/get-car-by-make-model/Toyota/Supra
```
- **Example Response:**
```json
    {
        "status": "success",
        "car": {
            "id": 1,
            "make": "Toyota",
            "model": "Supra",
            "year": 2020,
            "horsepower": 335,
            "weight": 3450.5,
            "zero_to_sixty": 4.1,
            "top_speed": 155,
            "handling": 8,
            "car_class": "Economy",
            "races": 2,
            "wins": 1
        }
    }
```

---

### **Route: `/api/race`**
- **Request Type:** GET  
- **Purpose:** Simulates a race between two cars.
- **Request Body:** None 
- **Response Format:** JSON  
  - `status` (String): response status - success or error
  - `message` (String): status description
  - `winner` (String): make and model of winning car 
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "message": "Race completed successfully", "winner": "Toyota Supra" }`
- **Example Response:**
```json
{ "status": "success", "message": "Race completed successfully", "winner": "Toyota Supra" }
```

---

### **Route: `/api/clear-track`**
- **Request Type:** POST  
- **Purpose:** Clears all cars from the race track.  
- **Response Format:** JSON  
  - `status` (String): response status - success or error
  - `message` (String): status description 
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "message": "Track cleared successfully" }`
- **Example Response:**
```json
{ "status": "success", "message": "Track cleared successfully" }
```

---

### **Route: `/api/enter-track`**
- **Request Type:** POST  
- **Purpose:** Adds a car to the race track.  
- **Request Body:**  
  - `car_id` (Integer): ID of the car to add  
- **Response Format:** JSON 
  - `status` (String): response status - success or error
  - `message` (String): status description
  - `cars_on_track` (Integer): number of total cars on track after car has been added  
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "message": "Toyota Supra entered the track", "cars_on_track": 2 }` 
- **Example Request:**
```json
{
  "car_id": 1
} 
```
- **Example Response:**
```json
{
  "status": "success",
  "message": "Toyota Supra entered the track", 
  "cars_on_track": 2 
 }
```

---

### **Route: `/api/get-cars`**
- **Request Type:** GET  
- **Purpose:** Retrieves all cars in the system.  
- **Response Format:** JSON 
  - `status` (String): response status - success or error
  - `count` (Integer): number of cars in the system
  - `cars` (Array of Objects): array of all cars  
    - `id`: unique identifier for car
    - `make` (String): car manufacturer
    - `model` (String): car model
    - `year` (Integer): year the car was produced
    - `horsepower` (Integer): horsepower of the car
    - `weight` (Float): weight of the car in pounds
    - `zero_to_sixty` (Float): 0-60 mph time in seconds
    - `top_speed` (Integer): top speed of car in miles per hour
    - `handling` (Integer): handling rating from 1-10
    - `car_class` (String): class of car
    - `races` (Integer): number of races participated in
    - `wins` (Integer): number of races won
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "count": 2, "cars": [ ... ] }`
- **Example Response:**
```json
{
  "status": "success",
  "count": 2,
  "cars": [
    {
      "id": 1,
      "make": "Toyota",
      "model": "Supra",
      "year": 2020,
      "horsepower": 335,
      "weight": 3450.5,
      "zero_to_sixty": 4.1,
      "top_speed": 155,
      "handling": 8,
      "car_class": "Economy",
      "races": 5,
      "wins": 3
    },
    {
      "id": 2,
      "make": "Ford",
      "model": "Mustang",
      "year": 2019,
      "horsepower": 450,
      "weight": 3700,
      "zero_to_sixty": 3.9,
      "top_speed": 155,
      "handling": 7,
      "car_class": "Sport",
      "races": 4,
      "wins": 2
    }
  ]
}

```

---

### **Route: `/api/leaderboard`**
- **Request Type:** GET  
- **Purpose:** Returns the leaderboard of cars by wins or win percentage.  
- **Query Parameters:**  
  - `sort_by` (String): Either `"wins"` or `"win_pct"` (optional, default is `"wins"`)  
- **Response Format:** JSON  
  - `status` (String): response status - success or error
  - `count` (Integer): number of cars on the leaderboard
  - `sort_by` (String): Either `"wins"` or `"win_pct"`
  - `leaderboard` (Array of Objects): List of cars sorted by the specified criterion, each containing:
    - `id`: unique identifier for car
    - `make` (String): car manufacturer
    - `model` (String): car model
    - `year` (Integer): year the car was produced
    - `horsepower` (Integer): horsepower of the car
    - `weight` (Float): weight of the car in pounds
    - `zero_to_sixty` (Float): 0-60 mph time in seconds
    - `top_speed` (Integer): top speed of car in miles per hour
    - `handling` (Integer): handling rating from 1-10
    - `car_class` (String): class of car
    - `races` (Integer): number of races participated in
    - `wins` (Integer): number of races won
    - `win_pct` (Float): percentage of races won (races won / races participated in * 100)
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "count": 3, "sort_by": "wins", "leaderboard": [ ... ] }`
- **Example Response:**
```json
{
  "status": "success",
  "count": 3,
  "sort_by": "wins",
  "leaderboard": [
    {
      "id": 2,
      "make": "Nissan",
      "model": "GT-R",
      "year": 2021,
      "horsepower": 565,
      "weight": 3900.0,
      "zero_to_sixty": 2.9,
      "top_speed": 196,
      "handling": 9,
      "car_class": "Sport",
      "races": 10,
      "wins": 7,
      "win_pct": 0.7
    },
    {
      "id": 1,
      "make": "Toyota",
      "model": "Supra",
      "year": 2020,
      "horsepower": 335,
      "weight": 3450.5,
      "zero_to_sixty": 4.1,
      "top_speed": 155,
      "handling": 8,
      "car_class": "Economy",
      "races": 5,
      "wins": 3,
      "win_pct": 0.6
    },
    {
      "id": 3,
      "make": "Mazda",
      "model": "Miata",
      "year": 2019,
      "horsepower": 181,
      "weight": 2345.0,
      "zero_to_sixty": 5.7,
      "top_speed": 135,
      "handling": 7,
      "car_class": "Sport",
      "races": 8,
      "wins": 2,
      "win_pct": 0.25
    }
  ]
}


```
---

### **Route: `/api/health`**
- **Request Type:** GET  
- **Purpose:** Basic health check for the server.  
- **Response Format:** JSON 
  - `status` (String): response status - success or error
  - `message` (String): status description
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "message": "Service is running" }`
- **Example Response:**
```json
{
  "status": "success",
  "message": "Service is running"
}
```

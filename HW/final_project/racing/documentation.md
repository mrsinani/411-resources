# API Route Documentation

---

### **Route: `/api/create-user`**
- **Request Type:** PUT  
- **Purpose:** Registers a new user account.  
- **Request Body:**  
  - `username` (String): Desired username  
  - `password` (String): Desired password  
- **Response Format:** JSON  
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
  - `make`, `model`, `year`, `horsepower`, `weight`, `zero_to_sixty`, `top_speed`, `handling`  
- **Response Format:** JSON  
  - **Success Response Example:**  
    - Code: 201  
    - Content: `{ "status": "success", "message": "Car 'Toyota Supra' added successfully", "car_class": "A" }`  
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
  "car_class": "A"
}
```

---

### **Route: `/api/delete-car/<car_id>`**
- **Request Type:** DELETE  
- **Purpose:** Deletes a car by its ID.  
- **Path Parameter:**  
  - `car_id` (Integer): Car's ID  
- **Response Format:** JSON  
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "message": "Car 'Toyota Supra' deleted successfully" }`

---

### **Route: `/api/get-car-by-id/<car_id>`**
- **Request Type:** GET  
- **Purpose:** Retrieves car details by ID.  
- **Path Parameter:**  
  - `car_id` (Integer): Car's ID  
- **Response Format:** JSON  
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "car": { ...car details... } }`

---

### **Route: `/api/get-car-by-make-model/<make>/<model>`**
- **Request Type:** GET  
- **Purpose:** Retrieves car details by make and model.  
- **Path Parameters:**  
  - `make` (String): Car make  
  - `model` (String): Car model  
- **Response Format:** JSON  
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "car": { ...car details... } }`

---

### **Route: `/api/race`**
- **Request Type:** GET  
- **Purpose:** Simulates a race between two cars.  
- **Response Format:** JSON  
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "message": "Race completed successfully", "winner": "Toyota Supra" }`

---

### **Route: `/api/clear-track`**
- **Request Type:** POST  
- **Purpose:** Clears all cars from the race track.  
- **Response Format:** JSON  
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "message": "Track cleared successfully" }`

---

### **Route: `/api/enter-track`**
- **Request Type:** POST  
- **Purpose:** Adds a car to the race track.  
- **Request Body:**  
  - `car_id` (Integer): ID of the car to add  
- **Response Format:** JSON  
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "message": "Toyota Supra entered the track", "cars_on_track": 2 }`  
- **Example Request:**
```json
{
  "car_id": 1
}
```

---

### **Route: `/api/get-cars`**
- **Request Type:** GET  
- **Purpose:** Retrieves all cars in the system.  
- **Response Format:** JSON  
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "count": 5, "cars": [ ... ] }`

---

### **Route: `/api/leaderboard`**
- **Request Type:** GET  
- **Purpose:** Returns the leaderboard of cars by wins or win percentage.  
- **Query Parameters:**  
  - `sort_by` (String): Either `"wins"` or `"win_pct"` (optional, default is `"wins"`)  
- **Response Format:** JSON  
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "count": 3, "sort_by": "wins", "leaderboard": [ ... ] }`

---

### **Route: `/api/health`**
- **Request Type:** GET  
- **Purpose:** Basic health check for the server.  
- **Response Format:** JSON  
  - **Success Response Example:**  
    - Code: 200  
    - Content: `{ "status": "success", "message": "Service is running" }`

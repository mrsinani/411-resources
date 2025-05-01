import requests


def run_smoketest():
    base_url = "http://localhost:5001/api"
    username = "test"
    password = "test"

    test_car_1 = {
        "make": "Audi",
        "model": "Q5",
        "year": 2014,
        "horsepower": 240,
        "weight": 4475,
        "zero_to_sixty": 6.5,
        "top_speed": 128,
        "handling": 8
    }

    test_car_2 = {
        "make": "Ford",
        "model": "Mustang",
        "year": 2019,
        "horsepower": 450,
        "weight": 3700,
        "zero_to_sixty": 3.9,
        "top_speed": 155,
        "handling": 7
    }

    # Health check
    health_response = requests.get(f"{base_url}/health")
    assert health_response.status_code == 200
    assert health_response.json()["status"] == "success"
    print("Health check successful")

    # Reset users
    delete_user_response = requests.delete(f"{base_url}/reset-users")
    assert delete_user_response.status_code == 200
    assert delete_user_response.json()["status"] == "success"
    print("Reset users successful")

    # Reset cars
    delete_cars_response = requests.delete(f"{base_url}/reset-cars")
    assert delete_cars_response.status_code == 200
    assert delete_cars_response.json()["status"] == "success"
    print("Reset cars successful")

    # Create user
    create_user_response = requests.put(f"{base_url}/create-user", json={
        "username": username,
        "password": password
    })
    assert create_user_response.status_code == 201
    assert create_user_response.json()["status"] == "success"
    print("User creation successful")

    session = requests.Session()

    # Log in
    login_resp = session.post(f"{base_url}/login", json={
        "username": username,
        "password": password
    })
    assert login_resp.status_code == 200
    assert login_resp.json()["status"] == "success"
    print("Login successful")

    # Add first car
    add_car_resp = session.post(f"{base_url}/add-car", json=test_car_1)
    assert add_car_resp.status_code == 201
    assert add_car_resp.json()["status"] == "success"
    print("First car creation successful")

    # Change password
    change_password_resp = session.post(f"{base_url}/change-password", json={
        "new_password": "new_password"
    })
    assert change_password_resp.status_code == 200
    assert change_password_resp.json()["status"] == "success"
    print("Password change successful")

    # Log in with new password
    login_resp = session.post(f"{base_url}/login", json={
        "username": username,
        "password": "new_password"
    })
    assert login_resp.status_code == 200
    assert login_resp.json()["status"] == "success"
    print("Login with new password successful")

    # Add second car
    add_car_resp = session.post(f"{base_url}/add-car", json=test_car_2)
    assert add_car_resp.status_code == 201
    assert add_car_resp.json()["status"] == "success"
    print("Second car creation successful")

    # Get all cars
    get_cars_resp = session.get(f"{base_url}/get-cars")
    assert get_cars_resp.status_code == 200
    cars = get_cars_resp.json()["cars"]
    assert len(cars) >= 2
    car1_id = cars[0]["id"]
    car2_id = cars[1]["id"]
    print("Get cars successful")

    # Enter both cars onto the track
    enter_track_resp1 = session.post(f"{base_url}/enter-track", json={"car_id": car1_id})
    assert enter_track_resp1.status_code == 200
    assert enter_track_resp1.json()["status"] == "success"
    print("First car entered track")

    enter_track_resp2 = session.post(f"{base_url}/enter-track", json={"car_id": car2_id})
    assert enter_track_resp2.status_code == 200
    assert enter_track_resp2.json()["status"] == "success"
    print("Second car entered track")

    # Simulate a race
    race_resp = session.get(f"{base_url}/race")
    assert race_resp.status_code == 200
    assert race_resp.json()["status"] == "success"
    print(f"Race successful, winner: {race_resp.json()['winner']}")

    # Log out
    logout_resp = session.post(f"{base_url}/logout")
    assert logout_resp.status_code == 200
    assert logout_resp.json()["status"] == "success"
    print("Logout successful")

    # Try to add a car while logged out (should fail)
    add_car_logged_out_resp = session.post(f"{base_url}/add-car", json=test_car_1)
    assert add_car_logged_out_resp.status_code == 401
    assert add_car_logged_out_resp.json()["status"] == "error"
    print("Car creation failed as expected when logged out")

if __name__ == "__main__":
    run_smoketest() 
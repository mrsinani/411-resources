import React, { useState, useEffect } from "react";

const API_BASE = "http://localhost:5001";

function App() {
  // Auth state
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [authMessage, setAuthMessage] = useState("");
  const [mainMessage, setMainMessage] = useState("");
  // Login/Register
  const [loginUsername, setLoginUsername] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [registerUsername, setRegisterUsername] = useState("");
  const [registerPassword, setRegisterPassword] = useState("");
  // Cars
  const [cars, setCars] = useState([]);
  const [make, setMake] = useState("");
  const [model, setModel] = useState("");
  const [year, setYear] = useState("");
  const [hp, setHp] = useState("");
  // Track
  const [carsOnTrack, setCarsOnTrack] = useState([]);

  // Check login on mount
  useEffect(() => {
    fetch(`${API_BASE}/api/get-cars`, { credentials: "include" })
      .then((res) => {
        if (res.status === 200) {
          setIsLoggedIn(true);
          return res.json();
        } else {
          setIsLoggedIn(false);
          return null;
        }
      })
      .then((data) => {
        if (data && data.cars) setCars(data.cars);
      });
  }, []);

  // Login handler
  const handleLogin = async (e) => {
    e.preventDefault();
    setAuthMessage("");
    const res = await fetch(`${API_BASE}/api/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        username: loginUsername,
        password: loginPassword,
      }),
    });
    const data = await res.json();
    if (res.status === 200) {
      setIsLoggedIn(true);
      setAuthMessage("");
      setLoginUsername("");
      setLoginPassword("");
      fetchCars();
    } else {
      setAuthMessage(data.message || "Login failed");
    }
  };

  // Register handler
  const handleRegister = async (e) => {
    e.preventDefault();
    setAuthMessage("");
    const res = await fetch(`${API_BASE}/api/create-user`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: registerUsername,
        password: registerPassword,
      }),
    });
    const data = await res.json();
    if (res.status === 201) {
      setAuthMessage("Registration successful! You can now log in.");
      setRegisterUsername("");
      setRegisterPassword("");
    } else {
      setAuthMessage(data.message || "Registration failed");
    }
  };

  // Logout handler
  const handleLogout = async () => {
    await fetch(`${API_BASE}/api/logout`, {
      method: "POST",
      credentials: "include",
    });
    setIsLoggedIn(false);
    setCars([]);
    setMainMessage("");
    setAuthMessage("Logged out.");
    setCarsOnTrack([]);
  };

  // Fetch cars
  const fetchCars = async () => {
    const res = await fetch(`${API_BASE}/api/get-cars`, {
      credentials: "include",
    });
    if (res.status === 200) {
      const data = await res.json();
      setCars(data.cars);
    }
  };

  // Add car handler
  const handleAddCar = async (e) => {
    e.preventDefault();
    setMainMessage("");
    const res = await fetch(`${API_BASE}/api/add-car`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({
        make,
        model,
        year,
        horsepower: hp,
        weight: 3000,
        zero_to_sixty: 6.0,
        top_speed: 120,
        handling: 7,
      }),
    });
    if (res.status === 201) {
      setMainMessage("Car added!");
      setMake("");
      setModel("");
      setYear("");
      setHp("");
      fetchCars();
    } else {
      const data = await res.json();
      setMainMessage(data.message || "Failed to add car");
    }
  };

  // Enter track handler
  const handleEnterTrack = async (carId) => {
    setMainMessage("");
    const res = await fetch(`${API_BASE}/api/enter-track`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      credentials: "include",
      body: JSON.stringify({ car_id: carId }),
    });
    const data = await res.json();
    if (res.status === 200) {
      setMainMessage(data.message || "Car entered the track!");
      setCarsOnTrack((prev) => [...new Set([...prev, carId])]);
    } else {
      setMainMessage(data.message || "Failed to enter track");
    }
  };

  // Race handler
  const handleRace = async () => {
    const res = await fetch(`${API_BASE}/api/race`, {
      method: "GET",
      credentials: "include",
    });
    if (res.status === 200) {
      const result = await res.json();
      alert("Race result: " + JSON.stringify(result));
      fetchCars();
      setCarsOnTrack([]); // Clear track after race
    } else {
      const data = await res.json();
      alert(data.message || "Failed to race cars.");
    }
  };

  return (
    <div style={{ fontFamily: "Arial, sans-serif", margin: "2em" }}>
      <h1>Racing App</h1>
      {!isLoggedIn ? (
        <div>
          <h2>Login</h2>
          <form onSubmit={handleLogin}>
            <input
              type="text"
              placeholder="Username"
              value={loginUsername}
              onChange={(e) => setLoginUsername(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={loginPassword}
              onChange={(e) => setLoginPassword(e.target.value)}
              required
            />
            <button type="submit">Login</button>
          </form>
          <h2>Register</h2>
          <form onSubmit={handleRegister}>
            <input
              type="text"
              placeholder="Username"
              value={registerUsername}
              onChange={(e) => setRegisterUsername(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Password"
              value={registerPassword}
              onChange={(e) => setRegisterPassword(e.target.value)}
              required
            />
            <button type="submit">Register</button>
          </form>
          {authMessage && <div style={{ color: "red" }}>{authMessage}</div>}
        </div>
      ) : (
        <div>
          <button onClick={handleLogout}>Logout</button>
          <h2>Add Car</h2>
          <form onSubmit={handleAddCar}>
            <input
              type="text"
              placeholder="Make"
              value={make}
              onChange={(e) => setMake(e.target.value)}
              required
            />
            <input
              type="text"
              placeholder="Model"
              value={model}
              onChange={(e) => setModel(e.target.value)}
              required
            />
            <input
              type="number"
              placeholder="Year"
              value={year}
              onChange={(e) => setYear(e.target.value)}
              required
            />
            <input
              type="number"
              placeholder="Horsepower"
              value={hp}
              onChange={(e) => setHp(e.target.value)}
              required
            />
            <button type="submit">Add Car</button>
          </form>
          <h2>Cars</h2>
          <ul>
            {cars.map((car) => (
              <li key={car.id || `${car.make}-${car.model}-${car.year}`}>
                {car.make} {car.model} ({car.year}) - HP: {car.horsepower}
                <button
                  style={{ marginLeft: "1em" }}
                  onClick={() => handleEnterTrack(car.id)}
                  disabled={carsOnTrack.includes(car.id)}
                >
                  {carsOnTrack.includes(car.id) ? "On Track" : "Enter Track"}
                </button>
              </li>
            ))}
          </ul>
          <button onClick={handleRace} disabled={carsOnTrack.length < 2}>
            Race All Cars
          </button>
          {mainMessage && <div style={{ color: "green" }}>{mainMessage}</div>}
        </div>
      )}
    </div>
  );
}

export default App;

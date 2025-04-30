import pytest
from unittest.mock import MagicMock
from models.cars_model import Cars

@pytest.fixture
def mock_db_session(monkeypatch):
    """Mock the SQLAlchemy DB session used in Cars methods."""
    mock_session = MagicMock()
    monkeypatch.setattr("cars_model.db.session", mock_session)
    return mock_session

def test_get_car_class_economy():
    """Test that low power-to-weight ratio results in 'Economy' classification."""
    assert Cars.get_car_class(80, 1200) == "Economy"

def test_get_car_class_invalid_hp():
    """Test that zero horsepower raises a ValueError."""
    with pytest.raises(ValueError, match="Horsepower must be greater than 0."):
        Cars.get_car_class(0, 1000)

def test_create_car_valid(mock_db_session):
    """Test valid car creation triggers DB session add and commit."""
    Cars.create_car("TestMake", "TestModel", 2020, 150, 3000.0, 5.5, 120, 7)
    assert mock_db_session.add.called
    assert mock_db_session.commit.called

def test_create_car_invalid_year():
    """Test that a year outside valid range raises ValueError."""
    with pytest.raises(ValueError, match="Invalid year"):
        Cars.create_car("Make", "Model", 1800, 100, 2000, 6, 100, 5)

def test_update_stats_win(mock_db_session):
    """Test updating stats with a 'win' increases both races and wins."""
    car = Cars("Make", "Model", 2020, 150, 3000, 5.0, 120, 7)
    car.update_stats("win")
    assert car.races == 1
    assert car.wins == 1

def test_update_stats_invalid_result():
    """Test invalid race result raises ValueError."""
    car = Cars("Make", "Model", 2020, 150, 3000, 5.0, 120, 7)
    with pytest.raises(ValueError, match="Result must be 'win' or 'loss'"):
        car.update_stats("draw")

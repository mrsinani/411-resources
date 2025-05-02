import time
import pytest
from racing.models.track_model import TrackModel
from racing.models.cars_model import Cars


@pytest.fixture
def track_model():
    return TrackModel()

@pytest.fixture
def sample_car1(session):
    car = Cars(
        make="Ferrari", model="F8 Tributo",
        horsepower=710, weight=1435,
        zero_to_sixty=2.9, top_speed=211,
        handling=9.5, year=2020
    )
    session.add(car)
    session.commit()
    return car

@pytest.fixture
def sample_car2(session):
    car = Cars(
        make="Lamborghini", model="Huracan EVO",
        horsepower=631, weight=1422,
        zero_to_sixty=2.9, top_speed=202,
        handling=9.2, year=2021
    )
    session.add(car)
    session.commit()
    return car

@pytest.fixture
def sample_cars(sample_car1, sample_car2):
    return [sample_car1, sample_car2]


def test_clear_track(track_model):
    track_model.track = [1, 2]
    track_model.clear_track()
    assert len(track_model.track) == 0

def test_clear_track_empty(track_model, caplog):
    with caplog.at_level("WARNING"):
        track_model.clear_track()
    assert "Attempted to clear an empty track." in caplog.text

def test_enter_track_adds_car(track_model, sample_car1):
    track_model.enter_track(sample_car1.id)
    assert sample_car1.id in track_model.track
    assert sample_car1.id in track_model._car_cache

def test_enter_track_full(track_model):
    track_model.track = [1, 2]
    with pytest.raises(ValueError, match="Track is full"):
        track_model.enter_track(3)

def test_get_cars_empty(track_model, caplog):
    with caplog.at_level("WARNING"):
        cars = track_model.get_cars()
    assert cars == []
    assert "Retrieving cars from an empty track." in caplog.text

def test_get_cars_with_cache(track_model, sample_car1, mocker):
    track_model.track.append(sample_car1.id)
    track_model._car_cache[sample_car1.id] = sample_car1
    track_model._ttl[sample_car1.id] = time.time() + 60

    mock = mocker.patch("racing.models.cars_model.Cars.get_car_by_id")
    cars = track_model.get_cars()

    assert cars[0] == sample_car1
    mock.assert_not_called()

def test_get_cars_refreshes_cache(track_model, sample_car1, mocker):
    track_model.track.append(sample_car1.id)
    mock_get = mocker.patch("racing.models.cars_model.Cars.get_car_by_id", return_value=sample_car1)

    track_model._car_cache[sample_car1.id] = mocker.Mock()
    track_model._ttl[sample_car1.id] = time.time() - 1  # expired TTL

    cars = track_model.get_cars()
    assert cars[0] == sample_car1
    mock_get.assert_called_once_with(sample_car1.id)

def test_get_performance_score(track_model, sample_car1):
    score = track_model.get_performance_score(sample_car1)
    assert isinstance(score, float)
    assert score > 0

def test_clear_cache(track_model, sample_car1):
    track_model._car_cache[sample_car1.id] = sample_car1
    track_model._ttl[sample_car1.id] = time.time() + 100
    track_model.clear_cache()
    assert track_model._car_cache == {}
    assert track_model._ttl == {}

def test_race_with_two_cars(track_model, sample_cars, mocker, caplog):
    for car in sample_cars:
        track_model.enter_track(car.id)

    mocker.patch("racing.models.track_model.TrackModel.get_cars", return_value=sample_cars)
    mocker.patch("racing.models.track_model.TrackModel.get_performance_score", side_effect=[500, 400])
    mocker.patch("racing.models.track_model.get_random", return_value=0.4)

    mock_update = mocker.patch("racing.models.cars_model.Cars.update_stats")

    winner = track_model.race()

    assert winner == f"{sample_cars[0].make} {sample_cars[0].model}"
    mock_update.assert_any_call("win")
    mock_update.assert_any_call("loss")
    assert len(track_model.track) == 0
    assert "The winner is:" in caplog.text

def test_race_with_insufficient_cars(track_model):
    with pytest.raises(ValueError, match="There must be two cars to start a race."):
        track_model.race()

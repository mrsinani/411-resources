import pytest
from boxing.models.ring_model import RingModel
from boxing.models.boxers_model import Boxer


@pytest.fixture
def boxer1():
    """Fixture providing a sample boxer."""
    return Boxer(id=1, name="Ali", weight=180, height=180, reach=74.5, age=30)


@pytest.fixture
def boxer2():
    """Fixture providing a second sample boxer."""
    return Boxer(id=2, name="Tyson", weight=220, height=178, reach=71.0, age=28)


@pytest.fixture
def ring_model():
    """Fixture providing a new instance of RingModel for each test."""
    return RingModel()


def test_ring_init(ring_model):
    """Test that a new ring is initialized empty."""
    assert len(ring_model.ring) == 0


def test_enter_ring(ring_model, boxer1):
    """Test that a boxer can enter the ring."""
    ring_model.enter_ring(boxer1)
    assert len(ring_model.ring) == 1
    assert ring_model.ring[0].name == "Ali"


def test_enter_ring_full(ring_model, boxer1, boxer2):
    """Test that an error is raised when a third boxer tries to enter the ring."""
    ring_model.enter_ring(boxer1)
    ring_model.enter_ring(boxer2)
    
    boxer3 = Boxer(id=3, name="Holyfield", weight=210, height=185, reach=77.5, age=32)
    
    with pytest.raises(ValueError, match="Ring is full, cannot add more boxers."):
        ring_model.enter_ring(boxer3)


def test_enter_ring_invalid_type(ring_model):
    """Test that an error is raised when trying to add a non-Boxer to the ring."""
    with pytest.raises(TypeError, match="Invalid type: Expected 'Boxer'"):
        ring_model.enter_ring("Not a boxer")


def test_get_boxers_empty(ring_model):
    """Test getting boxers from an empty ring."""
    boxers = ring_model.get_boxers()
    assert len(boxers) == 0


def test_get_boxers(ring_model, boxer1, boxer2):
    """Test getting boxers from the ring."""
    ring_model.enter_ring(boxer1)
    ring_model.enter_ring(boxer2)
    
    boxers = ring_model.get_boxers()
    assert len(boxers) == 2
    assert boxers[0].name == "Ali"
    assert boxers[1].name == "Tyson"


def test_clear_ring(ring_model, boxer1, boxer2):
    """Test clearing the ring."""
    ring_model.enter_ring(boxer1)
    ring_model.enter_ring(boxer2)
    assert len(ring_model.ring) == 2
    
    ring_model.clear_ring()
    assert len(ring_model.ring) == 0


def test_clear_empty_ring(ring_model):
    """Test clearing an already empty ring."""
    ring_model.clear_ring()  # Should not raise an error
    assert len(ring_model.ring) == 0


def test_get_fighting_skill(ring_model, boxer1):
    """Test calculating a boxer's fighting skill."""
    skill = ring_model.get_fighting_skill(boxer1)
    # Here we know the exact formula: (boxer.weight * len(boxer.name)) + (boxer.reach / 10)
    expected_skill = (180 * 3) + (74.5 / 10) - 0  # Name "Ali" is 3 chars, age is 30 so no modifier
    assert skill == expected_skill


def test_fight(ring_model, boxer1, boxer2, mocker):
    """Test a fight between two boxers."""
    ring_model.enter_ring(boxer1)
    ring_model.enter_ring(boxer2)
    
    # Mock get_random to return a predictable value
    mocker.patch("boxing.models.ring_model.get_random", return_value=0.2)
    
    # Mock update_boxer_stats to avoid database calls
    mock_update = mocker.patch("boxing.models.ring_model.update_boxer_stats")
    
    winner = ring_model.fight()
    
    # Check that update_boxer_stats was called twice (once for each boxer)
    assert mock_update.call_count == 2
    
    # Check that the ring was cleared
    assert len(ring_model.ring) == 0
    
    # Check that a winner name was returned
    assert winner in ["Ali", "Tyson"]


def test_fight_not_enough_boxers(ring_model, boxer1):
    """Test that an error is raised when trying to start a fight with only one boxer."""
    ring_model.enter_ring(boxer1)
    
    with pytest.raises(ValueError, match="There must be two boxers to start a fight."):
        ring_model.fight()

import pytest
import sqlite3
from contextlib import contextmanager

from boxing.models.boxers_model import (
    create_boxer,
    delete_boxer,
    get_boxer_by_id,
    get_boxer_by_name,
    get_leaderboard,
    update_boxer_stats,
    get_weight_class,
)


@pytest.fixture
def mock_cursor(mocker):
    """Fixture to provide a mock database cursor for testing."""
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_cursor.fetchall.return_value = []
    mock_conn.commit.return_value = None

    @contextmanager
    def mock_get_db_connection():
        yield mock_conn

    mocker.patch("boxing.models.boxers_model.get_db_connection", mock_get_db_connection)
    return mock_cursor


def test_create_boxer_valid(mock_cursor):
    """Test creating a valid boxer."""
    create_boxer("Ali", 180, 180, 74.5, 30)
    mock_cursor.execute.assert_any_call("SELECT 1 FROM boxers WHERE name = ?", ("Ali",))


def test_create_boxer_duplicate(mock_cursor):
    """Test error when creating a boxer with a duplicate name."""
    mock_cursor.fetchone.return_value = True
    with pytest.raises(ValueError, match="Boxer with name 'Ali' already exists"):
        create_boxer("Ali", 180, 180, 74.5, 30)


def test_create_boxer_invalid_inputs():
    """Test error when creating a boxer with invalid parameters."""
    with pytest.raises(ValueError):
        create_boxer("Bad", 100, 180, 70.0, 30)  # Invalid weight
    with pytest.raises(ValueError):
        create_boxer("Bad", 180, 0, 70.0, 30)    # Invalid height
    with pytest.raises(ValueError):
        create_boxer("Bad", 180, 180, 0, 30)     # Invalid reach
    with pytest.raises(ValueError):
        create_boxer("Bad", 180, 180, 70.0, 10)  # Invalid age


def test_delete_boxer_success(mock_cursor):
    """Test successfully deleting a boxer."""
    mock_cursor.fetchone.return_value = True
    delete_boxer(1)
    mock_cursor.execute.assert_any_call("DELETE FROM boxers WHERE id = ?", (1,))


def test_delete_boxer_invalid_id(mock_cursor):
    """Test error when deleting a boxer with an invalid ID."""
    mock_cursor.fetchone.return_value = None
    with pytest.raises(ValueError, match="Boxer with ID 999 not found"):
        delete_boxer(999)


def test_get_boxer_by_id_found(mock_cursor):
    """Test successfully retrieving a boxer by ID."""
    mock_cursor.fetchone.return_value = (1, "Ali", 180, 180, 74.5, 30)
    boxer = get_boxer_by_id(1)
    assert boxer.name == "Ali"


def test_get_boxer_by_id_not_found(mock_cursor):
    """Test error when retrieving a boxer with an invalid ID."""
    mock_cursor.fetchone.return_value = None
    with pytest.raises(ValueError, match="Boxer with ID 999 not found"):
        get_boxer_by_id(999)


def test_get_boxer_by_name_found(mock_cursor):
    """Test successfully retrieving a boxer by name."""
    mock_cursor.fetchone.return_value = (1, "Ali", 180, 180, 74.5, 30)
    boxer = get_boxer_by_name("Ali")
    assert boxer.name == "Ali"


def test_get_boxer_by_name_not_found(mock_cursor):
    """Test error when retrieving a boxer with a non-existent name."""
    mock_cursor.fetchone.return_value = None
    with pytest.raises(ValueError, match="Boxer 'Ghost' not found"):
        get_boxer_by_name("Ghost")


def test_get_leaderboard_by_wins(mock_cursor):
    """Test retrieving the leaderboard sorted by wins."""
    mock_cursor.fetchall.return_value = [
        (1, "Ali", 180, 180, 74.5, 30, 10, 8, 0.8),
        (2, "Tyson", 220, 178, 71.0, 28, 15, 14, 0.93),
    ]
    
    leaderboard = get_leaderboard(sort_by="wins")
    
    assert len(leaderboard) == 2
    assert leaderboard[0]["name"] == "Ali"
    assert leaderboard[0]["win_pct"] == 80.0  # 0.8 * 100
    assert leaderboard[1]["name"] == "Tyson"
    assert leaderboard[1]["win_pct"] == 93.0  # 0.93 * 100


def test_get_leaderboard_by_win_pct(mock_cursor):
    """Test retrieving the leaderboard sorted by win percentage."""
    mock_cursor.fetchall.return_value = [
        (1, "Ali", 180, 180, 74.5, 30, 10, 8, 0.8),
        (2, "Tyson", 220, 178, 71.0, 28, 15, 14, 0.93),
    ]
    
    leaderboard = get_leaderboard(sort_by="win_pct")
    
    assert len(leaderboard) == 2
    assert leaderboard[0]["name"] == "Ali"
    assert leaderboard[1]["name"] == "Tyson"


def test_get_leaderboard_invalid_sort(mock_cursor):
    """Test error when retrieving the leaderboard with an invalid sort parameter."""
    with pytest.raises(ValueError, match="Invalid sort_by parameter: invalid"):
        get_leaderboard(sort_by="invalid")


def test_update_boxer_stats_win(mock_cursor):
    """Test updating a boxer's stats with a win."""
    mock_cursor.fetchone.return_value = True
    update_boxer_stats(1, "win")
    mock_cursor.execute.assert_any_call(
        "UPDATE boxers SET fights = fights + 1, wins = wins + 1 WHERE id = ?", (1,)
    )


def test_update_boxer_stats_loss(mock_cursor):
    """Test updating a boxer's stats with a loss."""
    mock_cursor.fetchone.return_value = True
    update_boxer_stats(1, "loss")
    mock_cursor.execute.assert_any_call(
        "UPDATE boxers SET fights = fights + 1 WHERE id = ?", (1,)
    )


def test_update_boxer_stats_invalid_result():
    """Test error when updating a boxer's stats with an invalid result."""
    with pytest.raises(ValueError, match="Invalid result: draw"):
        update_boxer_stats(1, "draw")


def test_update_boxer_not_found(mock_cursor):
    """Test error when updating stats for a non-existent boxer."""
    mock_cursor.fetchone.return_value = None
    with pytest.raises(ValueError, match="Boxer with ID 999 not found"):
        update_boxer_stats(999, "win")


def test_get_weight_class():
    """Test getting the correct weight class for different weights."""
    assert get_weight_class(210) == "HEAVYWEIGHT"
    assert get_weight_class(170) == "MIDDLEWEIGHT"
    assert get_weight_class(140) == "LIGHTWEIGHT"
    assert get_weight_class(125) == "FEATHERWEIGHT"
    with pytest.raises(ValueError):
        get_weight_class(100)

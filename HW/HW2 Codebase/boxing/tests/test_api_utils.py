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
    create_boxer("Ali", 180, 180, 74.5, 30)
    mock_cursor.execute.assert_any_call("SELECT 1 FROM boxers WHERE name = ?", ("Ali",))


def test_create_boxer_duplicate(mock_cursor):
    mock_cursor.fetchone.return_value = True
    with pytest.raises(ValueError, match="Boxer with name 'Ali' already exists"):
        create_boxer("Ali", 180, 180, 74.5, 30)


def test_create_boxer_invalid_inputs():
    with pytest.raises(ValueError):
        create_boxer("Bad", 100, 180, 70.0, 30)
    with pytest.raises(ValueError):
        create_boxer("Bad", 180, 0, 70.0, 30)
    with pytest.raises(ValueError):
        create_boxer("Bad", 180, 180, 0, 30)
    with pytest.raises(ValueError):
        create_boxer("Bad", 180, 180, 70.0, 10)


def test_delete_boxer_success(mock_cursor):
    mock_cursor.fetchone.return_value = True
    delete_boxer(1)
    mock_cursor.execute.assert_any_call("DELETE FROM boxers WHERE id = ?", (1,))


def test_delete_boxer_invalid_id(mock_cursor):
    mock_cursor.fetchone.return_value = None
    with pytest.raises(ValueError, match="Boxer with ID 999 not found"):
        delete_boxer(999)


def test_get_boxer_by_id_found(mock_cursor):
    mock_cursor.fetchone.return_value = (1, "Ali", 180, 180, 74.5, 30)
    boxer = get_boxer_by_id(1)
    assert boxer.name == "Ali"


def test_get_boxer_by_id_not_found(mock_cursor):
    mock_cursor.fetchone.return_value = None
    with pytest.raises(ValueError, match="Boxer with ID 999 not found"):
        get_boxer_by_id(999)


def test_get_boxer_by_name_found(mock_cursor):
    mock_cursor.fetchone.return_value = (1, "Ali", 180, 180, 74.5, 30)
    boxer = get_boxer_by_name("Ali")
    assert boxer.name == "Ali"


def test_get_boxer_by_name_not_found(mock_cursor):
    mock_cursor.fetchone.return_value = None
    with pytest.raises(ValueError, match="Boxer 'Ghost' not found"):
        get_boxer_by_name("Ghost")


def test_update_boxer_stats_win(mock_cursor):
    mock_cursor.fetchone.return_value = True
    update_boxer_stats(1, "win")
    mock_cursor.execute.assert_any_call(
        "UPDATE boxers SET fights = fights + 1, wins = wins + 1 WHERE id = ?", (1,)
    )


def test_update_boxer_stats_loss(mock_cursor):
    mock_cursor.fetchone.return_value = True
    update_boxer_stats(1, "loss")
    mock_cursor.execute.assert_any_call(
        "UPDATE boxers SET fights = fights + 1 WHERE id = ?", (1,)
    )


def test_update_boxer_stats_invalid_result():
    with pytest.raises(ValueError, match="Invalid result: draw"):
        update_boxer_stats(1, "draw")


def test_get_weight_class():
    assert get_weight_class(210) == "HEAVYWEIGHT"
    assert get_weight_class(170) == "MIDDLEWEIGHT"
    assert get_weight_class(140) == "LIGHTWEIGHT"
    assert get_weight_class(125) == "FEATHERWEIGHT"
    with pytest.raises(ValueError):
        get_weight_class(100)

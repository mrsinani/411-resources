import pytest
import sqlite3

from boxing.utils.sql_utils import check_database_connection, check_table_exists, get_db_connection


@pytest.fixture
def mock_sqlite_connect(mocker):
    """Fixture that mocks the sqlite3.connect function."""
    mock_conn = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = None
    mock_cursor.execute.return_value = None
    mock_conn.close.return_value = None
    
    mocker.patch("sqlite3.connect", return_value=mock_conn)
    return mock_conn, mock_cursor


def test_check_database_connection_success(mock_sqlite_connect):
    """Test successful database connection check."""
    mock_conn, mock_cursor = mock_sqlite_connect
    
    check_database_connection()
    
    # Verify that connect was called and a query was executed
    sqlite3.connect.assert_called_once()
    mock_cursor.execute.assert_called_with("SELECT 1;")
    mock_conn.close.assert_called_once()


def test_check_database_connection_failure(mocker):
    """Test database connection check when connection fails."""
    # Mock sqlite3.connect to raise an error
    mocker.patch("sqlite3.connect", side_effect=sqlite3.Error("Connection failed"))
    
    with pytest.raises(Exception, match="Database connection error: Connection failed"):
        check_database_connection()


def test_check_table_exists_found(mock_sqlite_connect):
    """Test successful table existence check."""
    mock_conn, mock_cursor = mock_sqlite_connect
    mock_cursor.fetchone.return_value = ("boxers",)
    
    check_table_exists("boxers")
    
    # Verify that connect was called and a query was executed
    sqlite3.connect.assert_called_once()
    mock_cursor.execute.assert_called_with(
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?;",
        ("boxers",)
    )
    mock_conn.close.assert_called_once()


def test_check_table_exists_not_found(mock_sqlite_connect):
    """Test table existence check when table is not found."""
    mock_conn, mock_cursor = mock_sqlite_connect
    mock_cursor.fetchone.return_value = None
    
    with pytest.raises(Exception, match="Table 'unknown_table' does not exist."):
        check_table_exists("unknown_table")


def test_check_table_exists_error(mocker):
    """Test table existence check when database error occurs."""
    # Mock sqlite3.connect to raise an error
    mocker.patch("sqlite3.connect", side_effect=sqlite3.Error("Database error"))
    
    with pytest.raises(Exception, match="Table check error for 'boxers': Database error"):
        check_table_exists("boxers")


def test_get_db_connection(mock_sqlite_connect):
    """Test the get_db_connection context manager."""
    mock_conn, _ = mock_sqlite_connect
    
    with get_db_connection() as conn:
        assert conn == mock_conn
        
    # Check that close was called after exiting the context
    mock_conn.close.assert_called_once()


def test_get_db_connection_error_handling(mocker):
    """Test error handling in the get_db_connection context manager."""
    # Mock sqlite3.connect to raise an error
    mocker.patch("sqlite3.connect", side_effect=sqlite3.Error("Connection error"))
    
    with pytest.raises(sqlite3.Error, match="Connection error"):
        with get_db_connection():
            pass  # This should not be executed 
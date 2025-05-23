import pytest
from unittest.mock import MagicMock
from models.user_model import Users
from werkzeug.security import generate_password_hash

@pytest.fixture
def mock_db_session(monkeypatch):
    """Mock the SQLAlchemy DB session used in Users methods."""
    mock_session = MagicMock()
    monkeypatch.setattr("user_model.db.session", mock_session)
    return mock_session

def test_create_user_success(mock_db_session, monkeypatch):
    """Test creating a new user when username is available."""
    monkeypatch.setattr("user_model.Users.query", MagicMock(filter_by=MagicMock(return_value=MagicMock(first=lambda: None))))
    Users.create_user("newuser", "password123")
    assert mock_db_session.add.called
    assert mock_db_session.commit.called

def test_create_user_already_exists(monkeypatch):
    """Test creating a user with a taken username raises ValueError."""
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = Users("existing", "hash")
    monkeypatch.setattr("user_model.Users.query", mock_query)
    with pytest.raises(ValueError, match="already exists"):
        Users.create_user("existing", "pass")

def test_check_password_correct(monkeypatch):
    """Test correct password returns True."""
    hashed = generate_password_hash("secret")
    mock_user = Users("test", hashed)
    monkeypatch.setattr("user_model.Users.query", MagicMock(filter_by=MagicMock(return_value=MagicMock(first=lambda: mock_user))))
    assert Users.check_password("test", "secret") is True

def test_delete_user_not_found(monkeypatch):
    """Test deleting a non-existent user raises ValueError."""
    monkeypatch.setattr("user_model.Users.query", MagicMock(filter_by=MagicMock(return_value=MagicMock(first=lambda: None))))
    with pytest.raises(ValueError, match="does not exist"):
        Users.delete_user("ghost")

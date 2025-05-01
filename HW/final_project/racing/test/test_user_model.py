import pytest
from unittest.mock import MagicMock
from werkzeug.security import check_password_hash, generate_password_hash
from ..models.user_model import Users, db
from flask import Flask

@pytest.fixture(scope="module", autouse=True)
def app_context():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
        yield

@pytest.fixture
def mock_db_session(monkeypatch):
    mock_session = MagicMock()
    monkeypatch.setattr("racing.models.user_model.db.session", mock_session)
    return mock_session

def test_create_user_success(mock_db_session, monkeypatch):
    monkeypatch.setattr("racing.models.user_model.Users.query", MagicMock(filter_by=MagicMock(return_value=MagicMock(first=lambda: None))))
    Users.create_user("newuser", "password123")
    assert mock_db_session.add.called
    assert mock_db_session.commit.called

def test_create_user_already_exists(monkeypatch):
    mock_query = MagicMock()
    mock_query.filter_by.return_value.first.return_value = Users("existing", "hash")
    monkeypatch.setattr("racing.models.user_model.Users.query", mock_query)
    with pytest.raises(ValueError, match="already exists"):
        Users.create_user("existing", "pass")

def test_check_password_correct(monkeypatch):
    mock_user = Users("test", "irrelevant")
    mock_user.password_hash = generate_password_hash("secret")
    monkeypatch.setattr(
        "racing.models.user_model.Users.query",
        MagicMock(filter_by=MagicMock(return_value=MagicMock(first=lambda: mock_user)))
    )
    assert Users.check_password("test", "secret") is True

def test_delete_user_not_found(monkeypatch):
    monkeypatch.setattr("racing.models.user_model.Users.query", MagicMock(filter_by=MagicMock(return_value=MagicMock(first=lambda: None))))
    with pytest.raises(ValueError, match="does not exist"):
        Users.delete_user("ghost")

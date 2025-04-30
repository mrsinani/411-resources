import logging
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from racing.db import db
from racing.utils.logger import configure_logger


logger = logging.getLogger(__name__)
configure_logger(logger)


class Users(db.Model, UserMixin):
    """Represents a user in the system for authentication.

    This model is responsible for user authentication and login/logout functionality.
    It maps to the 'users' table in the database and stores usernames and 
    hashed passwords.

    The class inherits from UserMixin which provides default implementations of 
    all the required Flask-Login methods.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(100), nullable=False)

    def __init__(self, username, password_hash):
        """Initialize a new User instance.

        Args:
            username: The username of the user.
            password_hash: The hashed password of the user.
        """
        self.username = username
        self.password_hash = password_hash

    def get_id(self):
        """Override of the UserMixin get_id method.

        Returns the username as the user ID for Flask-Login purposes.

        Returns:
            str: The username of the user.
        """
        return self.username

    @classmethod
    def create_user(cls, username, password):
        """Create a new user with the given username and password.

        Args:
            username: The username of the user.
            password: The plain-text password of the user.

        Raises:
            ValueError: If a user with the same username already exists.
        """
        logger.info(f"Creating user: {username}")

        # Check if the username already exists
        if cls.query.filter_by(username=username).first():
            logger.error(f"User '{username}' already exists.")
            raise ValueError(f"User '{username}' already exists.")

        # Create a new user
        hashed_password = generate_password_hash(password)
        user = cls(username=username, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        logger.info(f"User '{username}' created successfully.")

    @classmethod
    def check_password(cls, username, password):
        """Check if the password is valid for the given username.

        Args:
            username: The username of the user.
            password: The plain-text password to check.

        Returns:
            bool: True if the password is valid, False otherwise.

        Raises:
            ValueError: If the user does not exist.
        """
        logger.info(f"Checking password for user: {username}")

        user = cls.query.filter_by(username=username).first()
        if not user:
            logger.error(f"User '{username}' does not exist.")
            raise ValueError(f"User '{username}' does not exist.")

        valid = check_password_hash(user.password_hash, password)
        if valid:
            logger.info(f"Password valid for user: {username}")
        else:
            logger.error(f"Invalid password for user: {username}")
        return valid

    @classmethod
    def update_password(cls, username, new_password):
        """Update the password for the given username.

        Args:
            username: The username of the user.
            new_password: The new plain-text password to set.

        Raises:
            ValueError: If the user does not exist.
        """
        logger.info(f"Updating password for user: {username}")

        user = cls.query.filter_by(username=username).first()
        if not user:
            logger.error(f"User '{username}' does not exist.")
            raise ValueError(f"User '{username}' does not exist.")

        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        logger.info(f"Password updated for user: {username}")

    @classmethod
    def delete_user(cls, username):
        """Delete the user with the given username.

        Args:
            username: The username of the user to delete.

        Raises:
            ValueError: If the user does not exist.
        """
        logger.info(f"Deleting user: {username}")

        user = cls.query.filter_by(username=username).first()
        if not user:
            logger.error(f"User '{username}' does not exist.")
            raise ValueError(f"User '{username}' does not exist.")

        db.session.delete(user)
        db.session.commit()
        logger.info(f"User '{username}' deleted successfully.") 
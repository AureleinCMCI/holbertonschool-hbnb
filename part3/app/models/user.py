import uuid
import re
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from extension import db
bcrypt = Bcrypt()


class User(db.Model):  # Héritage de db.Model obligatoire
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, first_name, last_name, email, username, password, is_admin=False):
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.username = username
        self.hash_password(password)
        self.is_admin = is_admin

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    @staticmethod
    def validate_name(name, field_name):
        """Ensure name is a non-empty string with max length of 50 characters"""
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{field_name} cannot be empty.")
        return name.strip()[:50]

    @staticmethod
    def validate_email(email):
        """Ensure email is in a valid format"""
        if not isinstance(email, str) or not email.strip():
            raise ValueError("Email cannot be empty.")
        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format.")
        return email.strip()

import uuid
import re
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()
""" Class to create an User"""

class User:
    def __init__(self, first_name, last_name, email, is_admin=False, id=None , ),:
        self.id = id if id else str(uuid.uuid4())  # Utilise l'ID fourni ou génère un nouveau
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.first_name = first_name[:50]
        self.last_name = last_name[:50]
        self.email = email
        self.is_admin = is_admin
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        password = db.Column(db.String(255), nullable=False)  

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

@staticmethod
def validate_name(name, field_name):
        """Ensure name is a non-empty string with max length of 50 characters"""
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{field_name} cannot be empty.")
        return name[:50]


@staticmethod
    
def validate_email(email):

        """Ensure email is in a valid format"""
        if not isinstance(email, str) or not email.strip():
            raise ValueError("Email cannot be empty.")

        email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format.")

        return email
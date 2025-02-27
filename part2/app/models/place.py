import uuid
from datetime import datetime
from models.user import User
from models.review import Review
from models.amenity import Amenity

""" Class to create a place """


class Place:
    def __init__(self, title, description, price, latitude, longitude, owner):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.title = title[:100]
        self.description = description
        self.price = max(0, price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = owner if isinstance(owner, User) else None
        self.reviews = []
        self.amenities = []

    def validate_title(self, title):
        """Ensure that title is not empty and not over 100 characters."""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty.")
        return title[:100]

    def validate_price(self, price):
        """Ensure that price is a positive number."""
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number.")
        return price

    def validate_latitude(self, latitude):
        """Ensure latitude is between -90 and 90."""
        if not isinstance(latitude, (int, float)):
            raise ValueError("Latitude must be a number.")
        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        return latitude

    def validate_longitude(self, longitude):
        """Ensure longitude is between -180 and 180."""
        if not isinstance(longitude, (int, float)):
            raise ValueError("Longitude must be a number.")

        if not (-180 <= longitude <= 180):
            raise ValueError("Longitude must be between -180 and 180.")

        return longitude

    def add_review(self, review):
        """Add a review to the place."""
        if isinstance(review, Review):
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if isinstance(amenity, Amenity) and amenity not in self.amenities:
            self.amenities.append(amenity)

import uuid
from datetime import datetime
from models.review import Review
from models.amenity import Amenity

""" Class to create a place """


class Place:
    def __init__(self, title, description, price,
                 latitude, longitude, owner_id):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner_id = owner_id
        self.reviews = []
        self.amenities = []

    def validate_title(self, title):
        """Ensure that title is not empty and not over 100 characters."""
        if not title or not title.strip():
            raise ValueError("Title cannot be empty.")
        return title[:100]

    def validate_price(self, price):
        """Ensure that price is not negative."""
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a non-negative number.")
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

    def to_dict(self):
        """Convert the Place object into a dictionary."""
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "reviews": [review.to_dict() for review in self.reviews]
            if hasattr(Review, "to_dict") else [review.id
                                                for review in self.reviews],
            "amenities": [amenity.to_dict() for amenity in self.amenities]
            if hasattr(Amenity, "to_dict") else
            [amenity.id for amenity in self.amenities],
        }

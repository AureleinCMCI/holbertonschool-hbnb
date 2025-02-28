import uuid
from datetime import datetime
from app.models.amenity import Amenity
from app.models.user import User
from app.models.review import Review

class Place:
    def __init__(self, title, description, price, latitude, longitude, owner_id, amenities):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.title = title[:100]  # Max length 100
        self.description = description
        self.price = max(0, price)  # Ensure positive price
        self.latitude = max(-90.0, min(90.0, latitude))
        self.longitude = max(-180.0, min(180.0, longitude))
        self.owner_id = owner_id
        self.reviews = []  # One-to-many relationship
        self.amenities = amenities  # List of amenity IDs

    def add_review(self, review):
        """Add a review to the place."""
        if isinstance(review, Review):
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if isinstance(amenity, Amenity) and amenity not in self.amenities:
            self.amenities.append(amenity)

import uuid
from datetime import datetime
from models.user import User
from models.place import Place

""" Class that creates reviews """



class Review:
    def __init__(self, text, user_id, place_id):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        """Ensure the text is not empty"""
        self.text = text if text and text.strip() else "No review provided"

        """Ensure rating is between 1 and 5"""
        self.rating = max(1, min(5, rating))

        """Ensure place is a valid instance of Place"""
        if isinstance(place, Place):
            self.place = place
        else:
            raise ValueError("Invalid place reference.")
        
        """Ensure user is a valid instance of User"""
        if isinstance(user, User):
            self.user = user
        else:
            raise ValueError("Invalid user reference.")

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()
        self.text = text
        self.user_id = user_id
        self.place_id = place_id

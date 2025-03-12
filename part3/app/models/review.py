import uuid
from datetime import datetime
from app.models.user import User  # ✅ Correct
from app.models.place import Place  # ✅ Correct

""" Class that creates reviews """


class Review:
    def __init__(self, text: str, user: User, place: Place, rating: int ,user_id,place_id ):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.user_id = user_id  # Ajout de 'user_id'
        self.place_id = place_id 
        self.user = user  # Attendre un objet utilisateur
        self.place = place
        # ✅ Ensure the text is not empty   
        self.text = text.strip() if text and text.strip() else "No review provided"

        # ✅ Ensure rating is between 1 and 5
        self.rating = max(1, min(5, rating))

        # ✅ Ensure place is a valid instance of Place
        if isinstance(place, Place):
            self.place = place
            self.place_id = place.id  # Stocke l'ID du lieu
        else:
            raise ValueError("Invalid place reference.")

        # ✅ Ensure user is a valid instance of User
        if isinstance(user, User):
            self.user = user
            self.user_id = user.id  # Stocke l'ID de l'utilisateur
        else:
            raise ValueError("Invalid user reference.")

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

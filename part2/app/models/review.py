import uuid
from datetime import datetime
from app.models.user import User  # ✅ Correct
from app.models.place import Place  # ✅ Correct

""" Class that creates reviews """

class Review:
    def __init__(self, text: str, rating: int, user=None, user_id=None, place=None, place_id=None):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        # ✅ Vérifier et stocker `user_id`
        if user and isinstance(user, User):
            self.user = user
            self.user_id = user.id
        elif user_id:
            self.user = None
            self.user_id = user_id
        else:
            raise ValueError("Un `user` ou `user_id` est obligatoire.")

        # ✅ Vérifier et stocker `place_id`
        if place and isinstance(place, Place):
            self.place = place
            self.place_id = place.id
        elif place_id:
            self.place = None
            self.place_id = place_id
        else:
            raise ValueError("Un `place` ou `place_id` est obligatoire.")

        # ✅ Vérifier `text`
        self.text = text.strip() if text and text.strip() else "No review provided"

        # ✅ Vérifier que `rating` est bien entre 1 et 5
        self.rating = max(1, min(5, rating))

    def save(self):
        '''
        Update the updated_at timestamp whenever the object is modified
        '''
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


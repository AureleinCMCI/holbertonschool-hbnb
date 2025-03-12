import uuid
from datetime import datetime

class Review:
    def __init__(self, text: str, rating: int, user_id: str, place_id: str):
        self.id = str(uuid.uuid4())
        self.text = text.strip() if text and text.strip() else "No review provided"
        self.rating = max(1, min(5, rating))
        self.user_id = user_id
        self.place_id = place_id
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def update(self, text=None, rating=None):
        if text:
            self.text = text.strip()
        if rating is not None:
            self.rating = max(1, min(5, rating))
        self.updated_at = datetime.now()
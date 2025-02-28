import uuid
from datetime import datetime
from app.models.user import User
from app.models.place import Place

class Review:
    def __init__(self, text, user_id, place_id):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.text = text
        self.user_id = user_id
        self.place_id = place_id

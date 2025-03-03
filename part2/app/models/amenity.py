import uuid

from datetime import datetime
""" Class that adds ametinies"""


class Amenity:
    def __init__(self, name,description=''):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.name = name[:50]
        self.description = description

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()


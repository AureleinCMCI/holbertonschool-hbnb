from app.models.place import Place
from app import db

class PlaceService:
    @staticmethod
    def create_place(data, user_id):
        place = Place(
            name=data['name'],
            description=data['description'],
            owner_id=user_id
        )
        db.session.add(place)
        db.session.commit()
        return place

    @staticmethod
    def update_place(place_id, data, user_id):
        place = Place.query.get(place_id)
        if not place or place.owner_id != user_id:
            return None

        place.name = data.get('name', place.name)
        place.description = data.get('description', place.description)
        db.session.commit()
        return place

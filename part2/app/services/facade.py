from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.user import User
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    #######################################################################
    # CRUD: USER
    #######################################################################
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        
        return user

    #######################################################################
    # CRUD: AMENITY
    #######################################################################
    def create_amenity(self, amenity_data):
        amenity = Amenity(
            name=amenity_data['name'],
            description=amenity_data.get('description', '')
        )
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        amenity.name = amenity_data.get('name', amenity.name)
        amenity.description = amenity_data.get('description', amenity.description)
        
        return amenity

    #######################################################################
    # CRUD: PLACE
    #######################################################################
    def create_place(self, place_data):
        place = Place(
            title=place_data['title'],
            description=place_data['description'],
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id'],
            amenities=place_data['amenities']
        )
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        owner = self.get_owner_of_place(place_id)
        amenities = self.get_amenities_of_place(place_id)

        place.owner = owner
        place.amenities = amenities

        return place

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if not place:
            return None

        place.title = place_data.get('title', place.title)
        place.description = place_data.get('description', place.description)
        place.price = place_data.get('price', place.price)
        place.latitude = place_data.get('latitude', place.latitude)
        place.longitude = place_data.get('longitude', place.longitude)
        
        return place

    #######################################################################
    # CRUD: REVIEW
    #######################################################################
    def create_review(self, review_data):
        review = Review(
            text=review_data['text'],
            user_id=review_data['user_id'],
            place_id=review_data['place_id']
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_reviews_by_place(self, place_id):
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        review.text = review_data.get('text', review.text)
        
        return review

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review)
            return True
        return False

    #######################################################################
    # HELPER FUNCTIONS
    #######################################################################
    def get_owner_of_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            return self.user_repo.get(place.owner_id)
        return None

    def get_amenities_of_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            return [self.amenity_repo.get(a_id) for a_id in place.amenities]
        return []

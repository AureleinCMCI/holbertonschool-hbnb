from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.user import User
from app.persistence.repository import InMemoryRepository
<<<<<<< HEAD
from app.models.user import User
from app.models.amenity import Amenity  # Assure-toi d'importer la classe Amenity
from app.models.place import Place  # Assure-toi d'importer la classe Place correctement
from datetime import datetime
from app.models.review import Review

=======
>>>>>>> fd2e00e248e8b6f632a25a4ea582b9d4ef730f3e

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
<<<<<<< HEAD
        self.owner_repo = InMemoryRepository()
        
########################################################################### crud :USER ##################################################################################


=======

    #######################################################################
    # CRUD: USER
    #######################################################################
>>>>>>> fd2e00e248e8b6f632a25a4ea582b9d4ef730f3e
    def create_user(self, user_data):
        user = User(
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            email=user_data["email"]
        )
        self.user_repo.add(user)  # Ajouter l'utilisateur en mémoire
        print(f"DEBUG: User created -> {user.__dict__}")  # Log pour vérifier
        return user

<<<<<<< HEAD
   
=======
>>>>>>> fd2e00e248e8b6f632a25a4ea582b9d4ef730f3e
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
<<<<<<< HEAD
    
 # Retourne l'équipement mis à jour
=======
>>>>>>> fd2e00e248e8b6f632a25a4ea582b9d4ef730f3e

    #######################################################################
    # CRUD: PLACE
    #######################################################################
    def create_place(self, place_data):
<<<<<<< HEAD
        """Créer un nouveau lieu en vérifiant l'existence du propriétaire."""
        owner_id = place_data.pop("owner_id", None)  # Supprime owner_id des données
        owner = self.get_user(owner_id) if owner_id else None  # Récupérer l'objet User

        # Créer l'objet Place avec l'objet User et non son ID
        place = Place(
            title=place_data["title"],
            description=place_data["description"],
            price=place_data["price"],
            latitude=place_data["latitude"],
            longitude=place_data["longitude"],
            owner_id=owner_id
        )

        self.place_repo.add(place)  # Ajouter le lieu au repo
=======
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
>>>>>>> fd2e00e248e8b6f632a25a4ea582b9d4ef730f3e
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

<<<<<<< HEAD
    def update_place(self, place_id, place_data = []):
        # Vérifie si la place existe
        place = self.place_repo.get(place_id)
        if not place:
            return None  # Place non trouvée

        # Vérification que place_data est un dictionnaire
        if isinstance(place_data, Place):  # Si place_data est un objet de type Place
            place_data = place_data.to_dict()  # Convertir en dictionnaire

        if not isinstance(place_data, dict):  # Si ce n'est toujours pas un dictionnaire
            raise TypeError(f"Erreur: place_data doit être un dictionnaire, mais reçu {type(place_data)}")

        # Met à jour les informations de la place
        place.title = place_data.get('title', place.title)
        place.description = place_data.get('description', place.description)
        place.price = place_data.get('price', place.price)
        place.latitude = place_data.get('latitude', place.latitude)
        place.longitude = place_data.get('longitude', place.longitude)

        # Sauvegarde les modifications (si vous utilisez une base de données, il faut commit ici)
        return place  # Retourne l'objet mis à jour

    def get_amenities_of_place(self, place_id):
        """Récupère les commodités d'un lieu via `amenity_repo`."""
        return self.amenity_repo.get_by_place_id(place_id)

    def save_place(self, place_id):
        """Met à jour la date de modification d'un lieu"""
        place = self.place_repo.get(place_id)
        if place:
            place.updated_at = datetime.now()
        return place
    

    def get_owner_of_place(self, place_id):
        """Récupère le propriétaire d'un lieu via owner_repo"""
        return self.owner_repo.get_by_place_id(place_id)  # Exemple

########################################## REVVIEEUWWWWWWWWWWWWWWWWWWWWWWWW ##########################################################
    def create_review(self, review_data):
        print(f"DEBUG: Checking User ID {review_data.user_id}, Place ID {review_data.place_id}")

        user = self.get_user(review_data.user_id)
        place = self.get_place(review_data.place_id)

        if not user:
            print(f"ERROR: User with ID {review_data.user_id} not found.")
            return {"error": f"Utilisateur avec ID {review_data.user_id} introuvable"}, 404
        if not place:
            print(f"ERROR: Place with ID {review_data.place_id} not found.")
            return {"error": f"Lieu avec ID {review_data.place_id} introuvable"}, 404

        review = Review(
            text=review_data.text,
            rating=review_data.rating,
            user=user,
            place=place
        )

        print(f"DEBUG: Review object created -> {review.to_dict()}")

        self.review_repo.add(review)
        self.review_repo.save()
        print(f"DEBUG: Review added to repository with ID {review.id}")

        return review


=======
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

>>>>>>> fd2e00e248e8b6f632a25a4ea582b9d4ef730f3e
    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_reviews_by_place(self, place_id):
<<<<<<< HEAD
        print(f"DEBUG: Fetching reviews for place_id {place_id}")  # Log l'ID du lieu

        all_reviews = self.review_repo.get_all()
        print(f"DEBUG: Total reviews found in system: {len(all_reviews)}")  # Log le nombre total d'avis

        # Assurez-vous que la comparaison se fait bien sur des strings
        reviews = [review.to_dict() for review in all_reviews if str(review.place_id) == str(place_id)]

        print(f"DEBUG: Reviews matching place_id {place_id} -> {reviews}")  # Log les avis trouvés

        if not reviews:
            print(f"WARNING: No reviews found for place_id {place_id}")  # Log si aucun avis n'est trouvé

        return reviews




    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)  # Récupération de l'avis en base
        if not review:
            return None  # Si l'avis n'existe pas, retournez None

        # 🔍 Ajout d'un print pour voir le type de review_data
        print(f"DEBUG: Type of review_data -> {type(review_data)}, Value -> {review_data}")

        # ✅ Transformation en dictionnaire si nécessaire
        if not isinstance(review_data, dict):
            review_data = review_data.__dict__

        # Mise à jour des champs seulement s'ils sont présents dans review_data
        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']
        if 'user_id' in review_data:
            review.user_id = review_data['user_id']
        if 'place_id' in review_data:
            review.place_id = review_data['place_id']

        self.review_repo.save(review)  # Sauvegarde des modifications en base

        return review  # Retourne l'objet mis à jour
  # Retourne l'objet mis à jour

=======
        return [review for review in self.review_repo.get_all() if review.place_id == place_id]

    def update_review(self, review_id, review_data):
        review = self.review_repo.get(review_id)
        if not review:
            return None

        review.text = review_data.get('text', review.text)
        
        return review
>>>>>>> fd2e00e248e8b6f632a25a4ea582b9d4ef730f3e

    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review)
            return True
        return False
<<<<<<< HEAD
    

    
    def add_review(self, review):
        """Add a review to the place."""
        if isinstance(review, Review):
            self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if isinstance(amenity, Amenity) and amenity not in self.amenities:
            self.amenities.append(amenity)
=======

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
>>>>>>> fd2e00e248e8b6f632a25a4ea582b9d4ef730f3e

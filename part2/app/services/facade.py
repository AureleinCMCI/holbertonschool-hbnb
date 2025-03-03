from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity  # Assure-toi d'importer la classe Amenity
from app.models.place import Place  # Assure-toi d'importer la classe Place correctement
from datetime import datetime
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.owner_repo = InMemoryRepository()
        
########################################################################### crud :USER ##################################################################################
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
        # Récupérer l'utilisateur à partir de l'ID
        user = self.user_repo.get(user_id)
        
        # Si l'utilisateur n'existe pas, retourner None
        if not user:
            return None
        
        # Mettre à jour les champs de l'utilisateur en fonction des données reçues
        user.first_name = user_data.get('first_name', user.first_name)
        user.last_name = user_data.get('last_name', user.last_name)
        user.email = user_data.get('email', user.email)
        
        # Si tu utilises une base de données ou un autre système de persistance, il te faut enregistrer la modification.
        # Ici, si tu utilises un stockage en mémoire, la mise à jour est implicite, mais si tu as besoin d'un `commit` dans la BD, tu l'ajoutes ici.
        
        # Retourner l'utilisateur mis à jour
        return user

############################################### ici on gére le crud de amenity################################################################################################
    def create_amenity(self, amenity_data):
        amenity = Amenity(
            name=amenity_data['name'],
            description=amenity_data.get('description', '')  # Gérer la description
        )
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)


    def get_all_amenity(self):
        return self.amenity_repo.get_all()


    def update_amenity(self, amenity_id, amenity_data):
        # Récupère l'équipement à partir de son ID
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None  # Si l'équipement n'existe pas, retourne None

        # Vérifier si amenity_data est un dictionnaire, sinon le convertir
        if isinstance(amenity_data, Amenity):
            amenity_data = amenity_data.__dict__

        if hasattr(amenity_data, 'to_dict'):
            amenity_data = amenity_data.to_dict()

        # Vérifie et met à jour les attributs
        if isinstance(amenity_data, dict):  # Assure que c'est bien un dictionnaire
            if 'name' in amenity_data:
                amenity.name = amenity_data['name']

            # Enregistre les modifications
            self.amenity_repo.update(amenity.id, amenity)
        
        return amenity
    
 # Retourne l'équipement mis à jour


##################################################################CRUD place #############################################################""""""
    def create_place(self, place_data):
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


    def delete_review(self, review_id):
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review)
            return True
        return False
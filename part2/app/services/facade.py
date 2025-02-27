from app.persistence.repository import InMemoryRepository
from app.models.User import User
from app.models.amenity import Amenity  # Assure-toi d'importer la classe Amenity
from app.models.place import Place  # Assure-toi d'importer la classe Place correctement

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        
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
        place = Place(**place_data)
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
            # Vérifie si la place existe
            place = self.place_repo.get(place_id)
            if not place:
                return None  # Place non trouvée
            # Met à jour les informations de la place
            place.title = place_data.get('title', place.title)
            place.description = place_data.get('description', place.description)
            place.price = place_data.get('price', place.price)
            place.latitude = place_data.get('latitude', place.latitude)
            place.longitude = place_data.get('longitude', place.longitude)
            # Sauvegarde les modifications (dans ce cas, c'est implicite avec un dictionnaire)
            # Si tu utilises une base de données, tu devrais ici appeler la méthode pour persister la mise à jour.
            return place  # Reto
    



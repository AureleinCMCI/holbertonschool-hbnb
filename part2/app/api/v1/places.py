from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})



########################## METHODE CREAT PLACE ET RECUPERE TOUTE LES PLACES ENREGISTR2ER #############################################################################
@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        # Récupérer les données envoyées dans la requête via `api.payload`
        place_data = api.payload
        
        # Validation des données
        if not place_data.get('title'):
            return {'error': 'Title is required'}, 400
        
        if not place_data.get('price') or place_data['price'] <= 0:
            return {'error': 'Price must be a positive number'}, 400
        
        if not (-90 <= place_data['latitude'] <= 90):
            return {'error': 'Latitude must be between -90 and 90'}, 400
        
        if not (-180 <= place_data['longitude'] <= 180):
            return {'error': 'Longitude must be between -180 and 180'}, 400
        
        new_place = facade.create_place(place_data)
        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'owner_id': new_place.owner_id,
            'amenities': new_place.amenities
        }, 201
        
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places()

        if not places:
            return {'message': 'No places found'}, 404

        place_list = [{
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude
        } for place in places]

        return place_list, 200


###################################################### CRUD PORU AFFICHE LES DETAIL D'UNE PLACES et  METRE A JOUR  ###################################################################################

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)  # Récupérer la place via le facade

        if not place:
            return {'error': 'Place not found'}, 404  # Retourner 404 si la place n'existe pas

        # Récupérer les détails de la place (inclure les informations supplémentaires si nécessaire)
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner_id,
            'amenities': place.amenities
        }, 200

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    #############################MISE A JOUR###############################################################################################""
    def put(self, place_id):
        place = facade.get_place(place_id)  # Correction du nom de la méthode
        if not place:
            return {'error': 'Place not found'}, 404  # Correction du nom "amenity" en "place"
        
        place_data = api.payload

        # Validation des données
        validations = [
            ('title', lambda p: p and len(p) > 0, 'Title is required and cannot be empty.'),
            ('price', lambda p: p and p > 0, 'Price must be a positive number.'),
            ('latitude', lambda p: p is not None and -90 <= p <= 90, 'Latitude must be between -90 and 90.'),
            ('longitude', lambda p: p is not None and -180 <= p <= 180, 'Longitude must be between -180 and 180.')
        ]

        # Validation des données
        for field, validate_fn, error_message in validations:
            if field not in place_data or not validate_fn(place_data.get(field)):
                return {'error': f'Invalid input data. "{field}" {error_message}'}, 400

        # Mise à jour des données
        place.title = place_data.get('title', place.title)
        place.description = place_data.get('description', place.description)
        place.price = place_data.get('price', place.price)
        place.latitude = place_data.get('latitude', place.latitude)
        place.longitude = place_data.get('longitude', place.longitude)

        # Mise à jour de la place dans la base de données via la façade
        facade.update_place(place_id, place)

        return {
            'message': 'Place updated successfully',
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude
        }, 200

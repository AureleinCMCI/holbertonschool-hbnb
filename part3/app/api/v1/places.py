from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.place_service import PlaceService

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})

@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Crée un lieu. Accessible uniquement aux utilisateurs connectés.
        """
        current_user = get_jwt_identity()  # Obtenir l'utilisateur authentifié
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

        # Création du lieu via PlaceService
        new_place = PlaceService.create_place(place_data, current_user['id'])
        return {
            'id': new_place.id,
            'title': new_place.title,
            'description': new_place.description,
            'price': new_place.price,
            'latitude': new_place.latitude,
            'longitude': new_place.longitude,
            'amenities': new_place.amenities
        }, 201

    @jwt_required()
    @api.response(200, 'Places retrieved successfully')
    @api.response(404, 'No places found')
    def get(self):
        """
        Récupère tous les lieux accessibles publiquement.
        """
        places = PlaceService.get_all_places()
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

@api.route('/<place_id>')
class PlaceResource(Resource):
    @jwt_required()
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Récupère les détails d'un lieu spécifique.
        """
        place = PlaceService.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'amenities': place.amenities
        }, 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """
        Modifie un lieu. Accessible uniquement au propriétaire.
        """
        current_user = get_jwt_identity()
        place_data = api.payload

        # Validation des données
        validations = [
            ('title', lambda p: p and len(p) > 0, 'Title is required and cannot be empty.'),
            ('price', lambda p: p and p > 0, 'Price must be a positive number.'),
            ('latitude', lambda p: p is not None and -90 <= p <= 90, 'Latitude must be between -90 and 90.'),
            ('longitude', lambda p: p is not None and -180 <= p <= 180, 'Longitude must be between -180 and 180.')
        ]
        for field, validate_fn, error_message in validations:
            if field not in place_data or not validate_fn(place_data.get(field)):
                return {'error': f'Invalid input data. "{field}" {error_message}'}, 400

        # Mise à jour du lieu via PlaceService
        updated_place = PlaceService.update_place(place_id, place_data, current_user['id'])
        if not updated_place:
            return {'error': 'Place not found or unauthorized'}, 404

        return {
            'id': updated_place.id,
            'title': updated_place.title,
            'description': updated_place.description,
            'price': updated_place.price,
            'latitude': updated_place.latitude,
            'longitude': updated_place.longitude,
            'amenities': updated_place.amenities
        }, 200

@api.route('/<place_id>/reviews')
class PlaceReviews(Resource):
    @jwt_required()
    @api.response(200, 'Reviews retrieved successfully')
    @api.response(404, 'No reviews found for this place')
    def get(self, place_id):
        """
        Récupère toutes les critiques pour un lieu spécifique.
        """
        reviews = PlaceService.get_reviews_by_place(place_id)
        if not reviews:
            return {'message': 'No reviews found for this place'}, 404

        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            } for review in reviews
        ], 200

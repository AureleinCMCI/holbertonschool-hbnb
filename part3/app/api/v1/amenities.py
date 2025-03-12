from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload

        if not amenity_data.get('name'):
            return {'error': 'Missing amenity name'}, 400

        description = amenity_data.get('description', '')  # Default à une chaîne vide si non fournie

    # Appel à la méthode de création en passant la description
        new_amenity = facade.create_amenity({
            'name': amenity_data['name'],
            'description': description
        })
        
        new_amenity = facade.create_amenity(amenity_data)
        return {'id': new_amenity.id, 'name': new_amenity.name , 'description': new_amenity.description}, 201 

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):

        amenities = facade.get_all_amenity()
        return [{'id': a.id, 'name': a.name} for a in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        return {'id': amenity.id, 'name': amenity.name}, 200
    
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')

    def put(self, amenity_id):
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'error': 'Amenity not found'}, 404
        
        amenity_data = api.payload

        if 'name' not in amenity_data or not amenity_data['name']:
            return {'error': 'Invalid input data. "name" is required and cannot be empty.'}, 400
        amenity.name = amenity_data['name']
        
        facade.update_amenity(amenity_id, amenity)

        return {
            'message': 'Amenity updated successfully', 
            'id': amenity.id, 
            'name': amenity.name
            }, 200


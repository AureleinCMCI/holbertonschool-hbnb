from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/api/v1/amenities/ ')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):

        pass

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):

        pass
@api.route('/api/v1/amenities/ ')
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
        return {'message': 'Amenity updated successfully', 'id': amenity.id, 'name': amenity.name}, 200


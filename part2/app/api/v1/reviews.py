from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')
facade = HBnBFacade()

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        review_data = api.payload

        # Validation des données
        if not review_data.get('text'):
            return {'error': 'Text is required'}, 400

        new_review = facade.create_review(review_data)
        return {
            'id': new_review.id,
            'text': new_review.text,
            'user_id': new_review.user_id,
            'place_id': new_review.place_id
        }, 201

    def get(self):
        reviews = facade.review_repo.get_all()
        if not reviews:
            return {'message': 'No reviews found'}, 404

        review_list = [{
            'id': review.id,
            'text': review.text,
            'user_id': review.user_id,
            'place_id': review.place_id
        } for review in reviews]

        return review_list, 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        return {
            'id': review.id,
            'text': review.text,
            'user_id': review.user_id,
            'place_id': review.place_id
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @api.response(500, 'Internal Server Error')
    def put(self, review_id):
        review_data = api.payload  # JSON reçu de la requête

        review = facade.get_review(review_id)  # Récupération de l'avis en base
        if not review:
            return {'error': 'Review not found'}, 404

        try:
            # Mise à jour des champs seulement si présents dans la requête
            if 'text' in review_data:
                review.text = review_data['text']
            if 'rating' in review_data:
                review.rating = review_data['rating']
            if 'user_id' in review_data:
                review.user_id = review_data['user_id']
            if 'place_id' in review_data:
                review.place_id = review_data['place_id']

            # Sauvegarde des modifications
            facade.update_review(review_id, review)

            return {
                'message': 'Review updated successfully',
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id
            }, 200
        except Exception as e:
            print(f"Error updating review: {e}")
            return {'message': 'Internal Server Error'}, 500



    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        success = facade.delete_review(review_id)
        if not success:
            return {'error': 'Review not found'}, 404

        return {'message': 'Review deleted successfully'}, 200
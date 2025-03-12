from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask import request, jsonify
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
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
        """Créer un nouvel avis (review)"""
        data = request.get_json()

        # Vérifier si la requête contient bien des données
        if not data:
            return {"error": "Requête JSON manquante"}, 400

        # Vérifier que tous les champs nécessaires sont présents
        required_fields = ["text", "rating", "user_id", "place_id"]
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return {"error": f"Champs obligatoires manquants: {', '.join(missing_fields)}"}, 400

        # ✅ Vérifier si l'utilisateur existe
        user = facade.user_repo.get(data["user_id"])
        if user is None:
            return {"error": f"Utilisateur avec ID {data['user_id']} introuvable"}, 404

        # ✅ Vérifier si le lieu existe
        place = facade.place_repo.get(data["place_id"])
        if place is None:
            return {"error": f"Lieu avec ID {data['place_id']} introuvable"}, 404

        try:
            # ✅ Créer et enregistrer le nouvel avis (review)
            new_review = Review(
                text=data["text"],
                rating=data["rating"],
                user_id=data["user_id"],
                place_id=data["place_id"]
            )

            # ✅ Ajouter et sauvegarder l'avis dans le repository
            facade.review_repo.add(new_review)
            facade.review_repo.save()  # 🔹 Assure que l'avis est bien stocké

            # ✅ Debugging: Vérifier si l'objet Review est bien stocké
            print(f"DEBUG: Review ajouté -> {new_review.to_dict()}")

            # ✅ Retourner les données de l'avis sous forme de dictionnaire (sans `jsonify()`)
            return new_review.to_dict(), 201

        except Exception as e:
            print(f"ERROR: Erreur lors de la création de l'avis - {str(e)}")
            return {"error": "Une erreur est survenue lors de la création de l'avis."}, 500


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
    

    
@api.route('/places/<place_id>/reviews')
class PlaceReviews(Resource):
    @api.response(200, 'Reviews retrieved successfully')
    @api.response(404, 'No reviews found for this place')
    def get(self, place_id):
        """Retrieve all reviews for a specific place"""
        print(f"DEBUG: Retrieving reviews for place ID: {place_id}")  # Debug

        reviews = facade.get_reviews_by_place(place_id)  # Utilisation de la méthode existante

        if not reviews:
            return {'message': 'No reviews found for this place'}, 404

        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating
            } for review in reviews
        ], 200

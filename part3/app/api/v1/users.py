from flask import request
from flask_restx import Api, Namespace, Resource, fields
from werkzeug.security import generate_password_hash
from flask_bcrypt import Bcrypt
from app.services import facade

api = Namespace('users', description='User operations')

bcrypt = Bcrypt()

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='password OF the user ', min_lenght=6)
})


def hash_password(password):
    return generate_password_hash(password)

#create UsersNames 
@api.route('/')
class UserList(Resource):
    @api.response(200, 'User list retrieved successfully')
    def get(self):
        """Retrieve the list of users"""
        users = facade.get_all_users()
        if not users:
            return {'message': 'No users found'}, 404

        user_list = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users]

        return user_list, 200
    # Méthode POST pour créer un utilisateur
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Créer un nouvel utilisateur avec un mot de passe haché"""
        user_data = request.json

        # Vérifier si l'utilisateur existe déjà
        if facade.get_user_by_email(user_data['email']):
            return {'message': 'Un utilisateur avec cet email existe déjà.'}, 400

        # Hacher le mot de passe
        hashed_password = hash_password(user_data['password'])

        # Créer un nouvel utilisateur
        new_user = {
            "first_name": user_data['first_name'],
            "last_name": user_data['last_name'],
            "email": user_data['email'],
            "password": hashed_password  # Stocker le mot de passe haché
        }

        # Enregistrement de l'utilisateur
        created_user = facade.create_user(new_user)

        return {
            "message": "Utilisateur enregistré avec succès",
            "id": created_user.id
        }, 201  # ✅ Ne pas retourner le mot de passe

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Obtenir les détails d'un utilisateur par ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
    
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    
    def put(self, user_id):
        """Update user details"""
        user_data = api.payload  # Récupérer les données à jour de l'utilisateur
        # Appeler la méthode update_user en passant les deux arguments
        updated_user = facade.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'User not found'}, 404
        return {'id': updated_user.id, 'first_name': updated_user.first_name, 'last_name': updated_user.last_name, 'email': updated_user.email}, 200


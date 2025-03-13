from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.admin_service import AdminService

# Création du namespace pour les utilisateurs
api = Namespace('users', description='User operations')

# Définir le modèle User pour valider et documenter les entrées
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @jwt_required()
    @api.response(200, 'User list retrieved successfully')
    def get(self):
        """
        Récupère la liste des utilisateurs. Réservé aux administrateurs.
        """
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Accès interdit'}, 403

        users = AdminService.get_all_users()
        if not users:
            return {'message': 'Aucun utilisateur trouvé'}, 404

        user_list = [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users]

        return user_list, 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    def post(self):
        """
        Crée un nouvel utilisateur. Réservé aux administrateurs.
        """
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Accès interdit'}, 403

        user_data = api.payload
        existing_user = AdminService.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email déjà enregistré'}, 400

        new_user = AdminService.create_user(user_data)
        return {
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'email': new_user.email
        }, 201

@api.route('/<user_id>')
class UserResource(Resource):
    @jwt_required()
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Récupère les détails d'un utilisateur par ID. Réservé aux administrateurs.
        """
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Accès interdit'}, 403

        user = AdminService.get_user(user_id)
        if not user:
            return {'error': 'Utilisateur non trouvé'}, 404

        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200

    @jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(200, 'User successfully updated')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """
        Met à jour les détails d'un utilisateur. Réservé aux administrateurs.
        """
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Accès interdit'}, 403

        user_data = api.payload
        updated_user = AdminService.update_user(user_id, user_data)
        if not updated_user:
            return {'error': 'Utilisateur non trouvé'}, 404

        return {
            'id': updated_user.id,
            'first_name': updated_user.first_name,
            'last_name': updated_user.last_name,
            'email': updated_user.email
        }, 200

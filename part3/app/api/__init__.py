from flask import Flask, Blueprint
from flask_restx import Api
from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns

# Création du Blueprint pour l'API v1
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Création de l'instance de l'API Flask-RESTx
api = Api(api_bp, title='HBnB API', version='1.0', description='API for HBnB')

# Ajout des Namespaces (endpoints)
api.add_namespace(users_ns, path='/users')
api.add_namespace(amenities_ns, path='/amenities')
api.add_namespace(places_ns, path='/places')

# Fonction pour créer l'application Flask
def create_app():
    app = Flask(__name__)
    app.register_blueprint(api_bp)  # Enregistrement du Blueprint dans l'application Flask
    return app
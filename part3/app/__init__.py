from flask import Flask
from flask_restx import Api
from config import DevelopmentConfig
from extension import db, bcrypt, migrate

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialisation des extensions APRÈS la configuration
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # Configuration de l'API
    api = Api(app, version="1.0", title="API Flask", description="Une API REST avec Flask-RESTx")

    # Enregistrement des namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    # Création des tables (important pour démarrer avec une DB valide)
    with app.app_context():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from config import DevelopmentConfig

# Initialisation des extensions sans les attacher immédiatement à une app
db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_class=DevelopmentConfig):
    """Factory function pour créer l'application Flask"""
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialiser les extensions
    db.init_app(app)
    bcrypt.init_app(app)

    # Création de l'API
    api = Api(app, version="1.0", title="API Flask", description="Une API REST avec Flask-RESTx")

    # Import des namespaces APRES l'initialisation pour éviter les imports circulaires
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns

    # Ajout des routes
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app

# Permet d'exécuter l'application uniquement si le script est exécuté directement
if __name__ == "__main__":
    app = create_app()
    app.config.from_object('config.DevelopmentConfig')  # Assure-toi que c'est bien la bonne config
    app.run(debug=True)

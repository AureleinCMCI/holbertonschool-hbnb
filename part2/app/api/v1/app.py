from flask import Flask
from flask_restx import Api
from api.v1.places import api as place_api
from api.v1.reviews import api as review_api

app = Flask(__name__)
api = Api(app, version='1.0', title='HBnB API', description='HBnB REST API')

api.add_namespace(place_api, path='/api/v1/places')
api.add_namespace(review_api, path='/api/v1/reviews')

if __name__ == '__main__':
    app.run(debug=True)

from flask import Blueprint, jsonify, request

place_blueprint = Blueprint('place_blueprint', __name__)

# Exemple de données en mémoire
places = []

# Route pour ajouter une place (POST)
@place_blueprint.route('', methods=['POST'])
def add_place():
    data = request.get_json()
    if not valid_place_data(data):
        return jsonify({"error": "Invalid data"}), 400

    new_place = {
        'id': len(places) + 1,
        'name': data.get('name'),
        'price': data.get('price'),
        'latitude': data.get('latitude'),
        'longitude': data.get('longitude'),
        'owner': data.get('owner')
    }
    places.append(new_place)
    return jsonify(new_place), 201

# Route pour lire toutes les places (GET)
@place_blueprint.route('', methods=['GET'])
def get_places():
    return jsonify(places)

# Route pour lire une place (GET)
@place_blueprint.route('/<int:place_id>', methods=['GET'])
def get_place(place_id):
    place = next((place for place in places if place['id'] == place_id), None)
    if place:
        return jsonify(place)
    return jsonify({'error': 'Place not found'}), 404

# Route pour mettre à jour une place (PUT)
@place_blueprint.route('/<int:place_id>', methods=['PUT'])
def update_place(place_id):
    place = next((place for place in places if place['id'] == place_id), None)
    if not place:
        return jsonify({'error': 'Place not found'}), 404

    data = request.get_json()
    if not valid_place_data(data):
        return jsonify({"error": "Invalid data"}), 400

    place.update({
        'name': data.get('name', place['name']),
        'price': data.get('price', place['price']),
        'latitude': data.get('latitude', place['latitude']),
        'longitude': data.get('longitude', place['longitude']),
        'owner': data.get('owner', place['owner'])
    })
    return jsonify(place)

def valid_place_data(data):
    required_fields = ['name', 'price', 'latitude', 'longitude', 'owner']
    return all(field in data for field in required_fields)

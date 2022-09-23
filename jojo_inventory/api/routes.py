from flask import Blueprint, request, jsonify
from jojo_inventory.helpers import token_required
from jojo_inventory.models import db, Stand, stand_schema, stands_schema

api = Blueprint('api', __name__, url_prefix = '/api')



@api.route('/getdata')
@token_required
def getdata(current_user_token):
    return {'name': 'lando'}


# CREATE Stand ENDPOINT
@api.route('/stands', methods = ['POST'])
@token_required
def create_stand(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    attack_type = request.json['attack_style']
    ability_type = request.json['ability_type']
    max_speed = request.json['max_speed']
    appearance = request.json['appearance']
    weight = request.json['weight']
    personality = request.json['personality']
    series = request.json['series']
    user_token = current_user_token.token

    print(f"User Token: {current_user_token.token}")

    stand = Stand(name, description, price, attack_type, ability_type, max_speed, appearance, weight, personality, series, user_token = user_token)

    db.session.add(stand)
    db.session.commit()

    response = stand_schema.dump(stand)

    return jsonify(response)


# Retrieve ONE Stand endpoint
@api.route('/stands/<id>', methods = ['GET'])
@token_required
def get_stand(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        stand = Stand.query.get(id)
        response = stand_schema.dump(stand)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Token Required'}), 401


#  Retrieve All Stands
@api.route('/stands', methods = ['GET']) 
@token_required
def get_stands(current_user_token):
    owner = current_user_token.token
    stands = Stand.query.filter_by(user_token = owner).all()
    response = stands_schema.dump(stands)
    return jsonify(response)

# Update Stand Endpoint
@api.route('/stands/<id>', methods = ['POST', 'PUT'])
@token_required
def update_stand(current_user_token, id):
    stand = Stand.query.get(id)    
    stand.name = request.json['name']
    stand.description = request.json['description']
    stand.price = request.json['price']
    stand.attack_style = request.json['attack_style']
    stand.ability_type = request.json['ability_type']
    stand.max_speed = request.json['max_speed']
    stand.appearance = request.json['appearance']
    stand.weight = request.json['weight']
    stand.personality = request.json['personality']
    stand.series = request.json['series']
    stand.user_token = current_user_token.token

    db.session.commit()
    response = stand_schema.dump(stand)
    return jsonify(response)

# Delete Stand Endpoint
@api.route('/stands/<id>', methods = ["DELETE"])
@token_required
def delete_stand(current_user_token, id):
    stand = Stand.query.get(id)
    db.session.delete(stand)
    db.session.commit()
    response = stand_schema.dump(stand)
    return jsonify(response)
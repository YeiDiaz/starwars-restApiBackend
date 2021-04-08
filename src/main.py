"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Character, Favorites

## Nos permite hacer las encripciones de contraseñas
# from werkzeug.security import generate_password_hash, check_password_hash

## Nos permite manejar tokens por authentication (usuarios) 
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

#from models import Person
app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/character', methods=['GET'])
def get_character():

    character_query = Character.query.all()
    
    results = list(map(lambda x: x.serialize(), character_query))

    return jsonify(results), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    
    planets_query = Planets.query.all()
    results = list(map(lambda x: x.serialize(), planets_query))
 
    return jsonify(results), 200

@app.route('/users', methods=['GET'])
def get_users():
    
    users_query = User.query.all()
    results = list(map(lambda x: x.serialize(), users_query))
 
    return jsonify(results), 200

@app.route('/character/<int:id>', methods=['GET'])
def get_oneCharacter(id):

    person = Character.query.get(id)    
    return jsonify(person.serialize()), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_onePlanet(id):

    planet = Planets.query.get(id)    
    return jsonify(planet.serialize()), 200

  #FAVORITOS ROUTER  

@app.route('/users/favorites', methods=['GET'])
def get_favorites():
    favorites = Favorites.query.filter_by(user_id = User.id)
    # favorites = Favorites.query.all()
    # print(favorites)
    
    results = list(map(lambda x: x.serialize(), favorites))
    # print(results)
    return jsonify(results), 200
    # return jsonify("hola"), 200

@app.route('/favorites', methods=["GET"])
def get_favorite():
    favorites = Favorites.query.all()
    results = list(map(lambda x: x.serialize(), favorites))
    return jsonify(results), 200

@app.route('/users/favorites', methods=['POST'])
@jwt_required()
def add_fav():
    
    email = get_jwt_identity()
    user = User.query.filter_by(email = email).first()
    # recibir info del request
    add_new_fav = request.get_json()
    newFav = Favorites(user_id=user.id, tipo=add_new_fav["tipo"],favorite_id=add_new_fav["favorite_id"])
    db.session.add(newFav)
    db.session.commit()

    return jsonify("All good"), 200

@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
def del_fav(favorite_id):

    # recibir info del request
    
    delete_favorite = Favorites.query.get(favorite_id)
    if delete_favorite is None:
        raise APIException('Label not found', status_code=404)

    db.session.delete(delete_favorite)
    db.session.commit()

    return jsonify("All good"), 200

#register
@app.route('/register', methods=["POST"])
def register():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        user = request.json.get("user", None)
        # last_name = request.json.get("last_name", None)
    

        if not email:
            return jsonify({"msg": "email is required"}), 400
        if not password:
            return jsonify({"msg": "Password is required"}), 400
        if not user:
            return jsonify({"msg": "username is required"}), 400
        # if not last_name:
        #     return jsonify({"msg": "Last name is required"}), 400
       

        user = User.query.filter_by(email=email).first()
        if user:
            return jsonify({"msg": "This username already exists"}), 400

        adduser = User()
        adduser.email = email
        adduser.last_name = last_name
        adduser.is_active = True
        adduser.password = password
        db.session.add(user)
        db.session.commit()

        return jsonify({"success": "Thanks. your register was successfully", "status": "true"}), 200
#login 
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.json.get("email", None)
        password = request.json.get("password", None)


        if not email:
            return jsonify({"msg": "Username is required"}), 400
        if not password:
            return jsonify({"msg": "Password is required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"msg": "Username/Password are incorrect"}), 401

        if not check_password(user.password, password):
            return jsonify({"msg": "Username/Password are incorrect"}), 401

        # crear el token
        access_token = create_access_token(identity=user.email)

        data = {
            "user": user.serialize(),
            "token": access_token
        }

        return jsonify(data), 200
    
@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    if request.method == 'GET':
        token = get_jwt_identity()
        return jsonify({"success": "Acceso a espacio privado", "usuario": token}), 200
# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

import os

from flask import Flask, request, jsonify

from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_raw_jwt, \
    jwt_refresh_token_required
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError

from config import Development

app = Flask(__name__)
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)
app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)
migrate = Migrate(app, db)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)

from models import User


blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


@app.route('/', methods=['POST'])
def create_user():
    if not request.is_json:
        return {'error': 'Only Json'}, 400
    arg = request.get_json()
    new_user = User()

    try:
        new_user.username = arg.get('username')
        new_user.password = arg.get('password')
        new_user.email = arg.get('email')
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        return {'message': e}, 400

    return {'message': 'user was created, pleas confrim your email address'}, 201


@app.route('/login', methods=['POST'])
def login():
    print(request.json.get('username', None))
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username == 'test' or password == 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    ret = {
        'access_token': create_access_token(identity=username),
        'refresh_token': create_refresh_token(identity=username)
    }
    return jsonify(ret), 200


@app.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


# Endpoint for revoking the current users refresh token
@app.route('/logout2', methods=['DELETE'])
@jwt_refresh_token_required
def logout2():
    jti = get_raw_jwt()['jti']
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


# This will now prevent users with blacklisted tokens from
# accessing this endpoint
@app.route('/protected', methods=['GET'])
@jwt_required
def protected():
    return jsonify({'hello': 'world'})


if __name__ == '__main__':
    app.run()

import os

from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from webargs import fields, validate
from webargs.flaskparser import use_kwargs, parser

import decimal
import datetime
from bson.dbref import DBRef
from bson.objectid import ObjectId

from flask_bcrypt import Bcrypt

import json

from server import models

app = Flask(__name__)
bcrypt = Bcrypt(app)

# app.url_map.strict_slashes = False

app.config.update(
    DEBUG=True,
    TESTING=True,
    MONGODB_SETTINGS={
        'HOST': 'localhost',
        'PORT': 27017,
        'DB': 'dockeeper-test',
        'TZ_AWARE': False,
    },
)

# Setup the Flask-JWT-Extended extension
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this!
jwt = JWTManager(app)


api = Api(app)  # , prefix="/api/v1")

db = MongoEngine(app)


class MongoEncoder(json.JSONEncoder):
    def default(self, value, **kwargs):
        if isinstance(value, ObjectId):
            return str(value)
        if isinstance(value, DBRef):
            return value.id
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        if isinstance(value, datetime.date):
            return value.strftime("%Y-%m-%d")
        if isinstance(value, decimal.Decimal):
            return str(value)
        return super(MongoEncoder, self).default(value, **kwargs)


@app.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username:
        return jsonify({"msg": "Missing username parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if username == 'test' or password == 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    user = models.User.objects(username=username)[0]
    if bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.username+" "+str(user.id))
        return jsonify(access_token=access_token), 200


@app.route('/register', methods=['POST'])
def register():
    user_json = request.get_json(silent=True)
    user = models.User.from_json(str(user_json).replace("'", "\""))
    user.password = str(bcrypt.generate_password_hash(user.password))[2:-1]
    user.save()
    return jsonify(user), 200


class PrivateResource(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return current_user, 200


class DocumentResource(Resource):
    args = {
        'parserId': fields.Str(
            required=True
        ),
    }

    @use_kwargs(args)
    @jwt_required
    def get(self, parserId):
        current_user = get_jwt_identity()
        user = models.UserRef(username=current_user.split()[0], id=current_user.split()[1])
        # check parser authen owner editor or viewer
        parser = models.Parser.objects(id=parserId)[0]
        if user not in parser.owners + parser.editors + parser.viewers:
            return "can't view", 401
        parserRef = models.ParserRef(id=parserId, name=parser.name)
        documents = models.Document.objects(parserRef=parserRef)
        # print(documents.to_json())
        return jsonify(results=documents)

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        user = models.UserRef(username=current_user.split()[0], id=current_user.split()[1])
        document_json = request.get_json(force=True)
        document = models.Document.from_json(str(document_json).replace("'", "\""))
        document.uploadBy = user
        document.save()
        return jsonify(document)


class ParserResource(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        current_user_username = current_user.split()[0]
        current_user_id = current_user.split()[1]
        parsers = models.Parser.objects(Q(owners=models.UserRef(username=current_user_username, id=current_user_id))\
                                        | Q(editors=models.UserRef(username=current_user_username, id=current_user_id)))
        # print(current_user, ObjectId(current_user), parsers.to_json())
        # return json.dumps(parsers.to_json(), allow_nan=False, cls=MongoEncoder), 200
        return jsonify(results=parsers)

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        current_user_username = current_user.split()[0]
        current_user_id = current_user.split()[1]
        parser_json = request.get_json(force=True)
        # print(str(parser_json).replace("'", "\""))
        parser = models.Parser.from_json(str(parser_json).replace("'", "\""))
        # {'username': current_user_username, 'id': current_user_id}
        parser.owners = [models.UserRef(username=current_user_username, id=current_user_id)]
        parser.save()
        return jsonify(parser)


api.add_resource(PrivateResource, '/private')
api.add_resource(DocumentResource, '/documents')
api.add_resource(ParserResource, '/parsers')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='127.0.0.1', port=port, debug=True)

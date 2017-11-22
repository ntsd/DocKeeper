import os

from flask import Flask, request
from flask_mongoengine import MongoEngine
from flask_mongorest import MongoRest
from flask_mongorest.views import ResourceView
from flask_mongorest.resources import Resource
from flask_mongorest import methods
from flask_mongorest import operators as ops

from server import models

app = Flask(__name__)

app.url_map.strict_slashes = False

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

db = MongoEngine(app)
api = MongoRest(app)


class RoleResource(Resource):
    document = models.Role


class UserResource(Resource):
    document = models.User
    related_resources = {
        'role': RoleResource,
    }


class DocumentResource(Resource):
    document = models.Document


class ParserRuleTypeResource(Resource):
    document = models.ParserRuleType


class ParserRuleResource(Resource):
    document = models.ParserRule
    related_resources = {
        'ruleType': ParserRuleTypeResource,
    }


class ParserResource(Resource):
    document = models.Parser
    related_resources = {
        'parserRules': ParserRuleResource,
        'documents': DocumentResource
    }
    filters = {
        'name': [ops.Exact, ops.Startswith],
        'editors': [ops.Contains, ops.Exact],
        'viewers': [ops.Exact],
        'owners': [ops.Exact],
    }


@api.register(name='users', url='/users/')
class UserView(ResourceView):
    resource = UserResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]


@api.register(name='documents', url='/documents/')
class DocumentView(ResourceView):
    resource = DocumentResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]


@api.register(name='parserrules', url='/parserrules/')
class ParserRuleView(ResourceView):
    resource = ParserRuleResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]


@api.register(name='parsers', url='/parsers/')
class ParserView(ResourceView):
    resource = ParserResource
    methods = [methods.Create, methods.Update, methods.Fetch, methods.List]

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(host='127.0.0.1', port=port)

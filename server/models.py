import datetime
from flask_mongoengine import MongoEngine

db = MongoEngine()


class Role(db.EmbeddedDocument):
    name = db.StringField()
    description = db.StringField()


class User(db.Document):
    username = db.StringField(unique=True, max_length=20, required=True)
    password = db.StringField(required=True)
    email = db.EmailField(unique=True, required=True)
    role = db.EmbeddedDocumentField(Role)
    # done = db.BooleanField(default=False)
    # pub_date = db.DateTimeField(default=datetime.datetime.now)


class Document(db.Document):
    name = db.StringField()
    path = db.StringField()


class ParserRuleType(db.EmbeddedDocument):
    name = db.StringField()
    description = db.StringField()


class ParserRule(db.Document):
    name = db.StringField()
    ruleType = db.EmbeddedDocumentField(ParserRuleType, required=True)
    data = db.StringField()


class Parser(db.Document):
    name = db.StringField(required=True)
    owners = db.ListField(db.ReferenceField(User))
    editors = db.ListField(db.ReferenceField(User))
    viewers = db.ListField(db.ReferenceField(User))
    tags = db.ListField(db.StringField())
    documents = db.ListField(db.ReferenceField(Document))
    parserRules = db.ListField(db.ReferenceField(ParserRule))
    classificationData = db.BinaryField()

from datetime import datetime
from flask_mongoengine import MongoEngine
from bson.objectid import ObjectId

db = MongoEngine()


class Role(db.EmbeddedDocument):
    name = db.StringField()
    description = db.StringField()


class User(db.Document):
    username = db.StringField(unique=True, max_length=20, required=True)
    password = db.StringField(required=True)
    email = db.EmailField(unique=True, required=True)
    role = db.EmbeddedDocumentField(Role)
    updated_at = db.DateTimeField(default=datetime.now)
    created_at = db.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(User, self).save(*args, **kwargs)


class UserRef(db.EmbeddedDocument):
    username = db.StringField()
    id = db.ReferenceField(User)


class ParserRule(db.EmbeddedDocument):
    oid = db.ObjectIdField(required=True, default=lambda: ObjectId())
    name = db.StringField(required=True)
    ruleType = db.StringField()
    data = db.StringField()
    description = db.StringField()


class ExtractedRule(db.EmbeddedDocument):
    name = db.StringField()
    ruleType = db.StringField()
    data = db.StringField()


class Parser(db.Document):
    name = db.StringField(required=True)
    description = db.StringField()
    owners = db.ListField(db.EmbeddedDocumentField(UserRef))
    editors = db.ListField(db.EmbeddedDocumentField(UserRef))
    viewers = db.ListField(db.EmbeddedDocumentField(UserRef))
    tags = db.ListField(db.StringField())
    parserRules = db.ListField(db.EmbeddedDocumentField(ParserRule))
    classificationData = db.BinaryField()
    updated_at = db.DateTimeField(default=datetime.now)
    created_at = db.DateTimeField(default=datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(Parser, self).save(*args, **kwargs)


class ParserRef(db.EmbeddedDocument):
    name = db.StringField()
    id = db.ReferenceField(Parser)


class ExtractedData(db.DynamicEmbeddedDocument):
    pass


class Document(db.DynamicDocument):
    name = db.StringField()
    path = db.StringField()
    imagePaths = db.ListField(db.StringField())
    uploadBy = db.EmbeddedDocumentField(UserRef)
    parserRef = db.EmbeddedDocumentField(ParserRef)
    updated_at = db.DateTimeField(default=datetime.now)
    created_at = db.DateTimeField(default=datetime.now)
    # extracted = db.EmbeddedDocumentField(ExtractedData)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.now()
        self.updated_at = datetime.now()
        return super(Document, self).save(*args, **kwargs)

import os, shutil

from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort
from flask_mongoengine import MongoEngine
from mongoengine.queryset.visitor import Q
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity, create_refresh_token,
    jwt_refresh_token_required, get_raw_jwt
)
# from webargs import fields, validate
# from webargs.flaskparser import use_kwargs, parser
from werkzeug.utils import secure_filename

import decimal
import datetime
from bson.dbref import DBRef
from bson.objectid import ObjectId

from flask_bcrypt import Bcrypt

# for ocr
from utils import ImageOCR, RuleTypesExtract, PDF2Image
from utils import ImageFeatureExtraction
# from PIL import Image, ImageEnhance, ImageFilter

import json

import models

from flask_cors import CORS

import numpy as np

app = Flask(__name__)

CORS(app)

bcrypt = Bcrypt(app)

# app.url_map.strict_slashes = False

DOCUMENTS_FOLDER = 'static/documents/'
ALLOWED_EXTENSIONS = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif']
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config.update(
    DEBUG=True,
    TESTING=True,
    MONGODB_SETTINGS={
        'HOST': 'localhost',
        'PORT': 27017,
        'DB': 'dockeeper-test',
        'TZ_AWARE': False,
    },
    DOCUMENTS_FOLDER=DOCUMENTS_FOLDER
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


@app.route('/users/login', methods=['POST'])
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
        expires = datetime.timedelta(days=7)
        access_token = create_access_token(identity=user.username+" "+str(user.id), expires_delta=expires)
        return jsonify(access_token=access_token), 200


# @app.route('/logout', methods=['DELETE'])
# @jwt_required
# def logout():
#     jti = get_raw_jwt()['jti']
#     blacklist.add(jti)
#     return jsonify({"msg": "Successfully logged out"}), 200


@app.route('/users/register', methods=['POST'])
def register():
    user_json = request.get_json(silent=True)
    user = models.User.from_json(str(user_json).replace("'", "\""))
    user.password = str(bcrypt.generate_password_hash(user.password))[2:-1]
    user.save()
    return jsonify(user), 200

@app.route('/users/me', methods=['GET'])
@jwt_required
def me():
    current_user = get_jwt_identity()
    current_user_username, current_user_id = current_user.split()
    user = models.User.objects(id=current_user_id).get()
    return jsonify(user), 200


class PrivateResource(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        return current_user, 200


class DocumentsListResource(Resource):
    @jwt_required
    def get(self, parserId):
        current_user = get_jwt_identity()
        user = models.UserRef(username=current_user.split()[0], id=current_user.split()[1])
        # check parser authen owner editor or viewer
        parser = models.Parser.objects(id=parserId).get()
        if user not in parser.owners + parser.editors + parser.viewers:
            abort(401, description="you don't have permission.")
        # parserRef = models.ParserRef(id=parserId, name=parser.name) no need cuz find only by id
        documents = models.Document.objects(parserRef__id=parserId)
        # print(documents.to_json())
        return jsonify(results=documents)


class DocumentAddResource(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()  # todo need to check permission of parser
        user = models.UserRef(username=current_user.split()[0], id=current_user.split()[1])
        document_json = request.get_json(force=True)
        # print(document_json)
        document = models.Document.from_json(str(document_json).replace("'", "\""))
        document.uploadBy = user
        document.save()
        return jsonify(document)

from sklearn.neighbors.nearest_centroid import NearestCentroid

class DocumentRecommendResource(Resource):
    @jwt_required
    def get(self, documentId):
        nearestCentroid = NearestCentroid()
        X_train=[]
        y_train=[]

        current_user = get_jwt_identity()
        current_user_username = current_user.split()[0]
        current_user_id = current_user.split()[1]
        parsers = models.Parser.objects(Q(owners=models.UserRef(username=current_user_username, id=current_user_id)) \
                                        | Q(editors=models.UserRef(username=current_user_username, id=current_user_id)) \
                                        | Q(viewers=models.UserRef(username=current_user_username, id=current_user_id)))

        # parserDict={}
        for parser in parsers:
            docs = models.Document.objects(parserRef__id=parser.id)
            for doc in docs:
                for featurePath in doc.imageFeatures:
                    # print(featurePath)
                    X_train.append(np.load(featurePath))
                    y_train.append(parser.name)
            # parserDict[parser.name] = parser

        nearestCentroid.fit(X_train, y_train)

        document = models.Document.objects(id=documentId).get()

        Features = ImageFeatureExtraction.getFeaturesFromFile(document.imagePaths[0])
        predict = nearestCentroid.predict(Features)[0]
        # print(predict, parserDict[predict])
        return jsonify(predictParserName=predict) #, predictParser=parserDict[predict])

    @jwt_required
    def post(self): #todo
        file = request.files['document-file']
        fileName = secure_filename(file.filename)
        fileFullPath = os.path.join('tmp/',fileName)
        file.save(fileFullPath)
        if fileName[-4:] == '.pdf':  # if it pdf
            jpgFilePath = fileFullPath[:-4]+'.jpg'
            PDF2Image.pdf2image(fileFullPath, jpgFilePath)  # convert pdf to image
        else:
            jpgFilePath = fileFullPath
        Features = ImageFeatureExtraction.getFeaturesFromFile(jpgFilePath)


class DocumentExtractResource(Resource):  # todo extract only Rule or Main or All for 1 doc
    @jwt_required
    def get(self, documentId):   # todo need to check permission of parser
        document = models.Document.objects(id=documentId).get()
        # models.Document.objects(id=documentId).update_one(textOCR=text)
        extractedDataList = []
        for imagePath in document.imagePaths:
            # load image
            im = ImageOCR.Image.open(imagePath) # ImageOCR.cv2.imread(document.path)
            # load parser
            # print(document.parserRef.id.id)
            parserRules = models.Parser.objects(id=document.parserRef.id.id).get().parserRules
            extractedRules = []
            for rule in parserRules: # todo need to crop img
                #  im_out = ImageOCR.preprocess(im)
                data = RuleTypesExtract.extractProcess(rule, im)  # ImageOCR.pytesseract.image_to_string(im_out, lang='eng')  #+tha')
                extractedRule = models.ExtractedRule()
                extractedRule.name = rule.name
                extractedRule.data = data
                extractedRule.ruleType = rule.ruleType
                extractedRules.append(extractedRule)
            extractedData = models.ExtractedData()
            extractedData.extractedRules = extractedRules
            extractedDataList.append(extractedData)
        # extractedData.full_text = text # no need to extract fulltext anymore
        document.extracted = extractedDataList
        document.save()
        return jsonify(extractedDataList)

class DocumentExtractPreviewResource(Resource):
    def post(self, documentId):
        document = models.Document.objects(id=documentId).get()
        im = ImageOCR.Image.open(document.imagePaths[0])
        parserRule_json = request.get_json(force=True)
        # print(parserRule_json)
        parserRule = models.ParserRule.from_json(str(parserRule_json).replace("'", "\""))
        previewExtractRule = models.ExtractedRule()
        previewExtractRule.name = parserRule.name
        previewExtractRule.data = RuleTypesExtract.extractProcess(parserRule, im)
        # print(previewExtractRule.data)
        previewExtractRule.ruleType = parserRule.ruleType
        return jsonify([previewExtractRule])

class DocumentUploadResource(Resource):
    @jwt_required
    def post(self, documentId):   # todo need to check permission of parser
        # print(request.form, request.files)
        file = request.files['document-file']
        # parserId = request.form['parserId']
        fileName = secure_filename(file.filename)
        filePath = os.path.join(app.config['DOCUMENTS_FOLDER'], documentId)
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            os.makedirs(filePath+'/images')
            os.makedirs(filePath+'/hogs')
        fileFullPath = os.path.join(filePath, fileName)  # os.path.join(filePath, filename)
        file.save(fileFullPath)
        if fileName[-4:] == '.pdf':  # if it pdf
            PDF2Image.pdf2image(fileFullPath, os.path.join(filePath, 'images/image.jpg'))  # convert pdf to image
        else:
            PDF2Image.pdf2image(fileFullPath, os.path.join(filePath, 'images/image.jpg'))
            # file.save(os.path.join(filePath, 'images/image'+fileName[-4:]))  # this is preview path + file signature
        # update document db
        document = models.Document.objects(id=documentId).get()
        document.path = fileFullPath
        # get path of all image
        imagePaths = []
        for file in os.listdir(filePath+'/images'):
            if file.endswith(".jpg"):
                imagePaths.append(os.path.join(filePath+'/images', file))
        document.imagePaths = imagePaths

        count = len(imagePaths)

        # Image featuer extraction
        imageFeaturesPaths=[]
        for i in range(count):
            imageFeaturesPath = os.path.join(filePath, 'hogs/imageFeatures{}'.format(i))
            Features = ImageFeatureExtraction.getFeaturesFromFile(imagePaths[i])
            np.save(imageFeaturesPath, Features)
            imageFeaturesPaths.append(imageFeaturesPath+'.npy')
        document.imageFeatures = imageFeaturesPaths

        document.save()
        # models.Document.objects(id=documentId).update_one(path=fileFullPath)

        return jsonify(fileFullPath)


class DocumentResource(Resource):
    @jwt_required
    def get(self, documentId):
        document = models.Document.objects(id=documentId).get()   # todo need to check permission of parser
        # for extract in document.extracted:
        #     for data in extract.extractedRules:
        #         print(data._cls)
        #         data._cls = None
        return jsonify(document)

    @jwt_required
    def put(self, documentId):
        document = models.Document.objects(id=documentId).get()   # todo need to check permission of parser
        document_json = request.get_json(force=True)
        for (key, val) in document_json.items():
            # print(key, val)
            if key == "parserRef":
                document[key] = models.ParserRef.from_json(str(val).replace("'", "\""))
            elif key in ["uploadBy"]:
                document[key] = models.UserRef.from_json(str(val).replace("'", "\""))
            elif key in ["updated_at", "created_at", "_id"]:
                pass
            else:
                document[key] = val
        document.save()
        return jsonify(document)

    @jwt_required
    def delete(self, documentId):
        document = models.Document.objects(id=documentId)   # todo need to check permission of parser
        # to delete folder
        if document.get().path:
            folder = document.get().path.split('\\')[0]
            shutil.rmtree(folder)
            # for the_file in os.listdir(folder):
            #     file_path = os.path.join(folder, the_file)
            #     try:
            #         if os.path.isfile(file_path):
            #             os.unlink(file_path)
            #         #elif os.path.isdir(file_path): shutil.rmtree(file_path)
            #     except Exception as e:
            #         print(e)

        document.delete()

        return jsonify('deleted')


class ParsersListResource(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        current_user_username = current_user.split()[0]
        current_user_id = current_user.split()[1]
        parsers = models.Parser.objects(Q(owners=models.UserRef(username=current_user_username, id=current_user_id))\
                                        | Q(editors=models.UserRef(username=current_user_username, id=current_user_id))\
                                        | Q(viewers=models.UserRef(username=current_user_username, id=current_user_id)))
        # print(current_user, ObjectId(current_user), parsers.to_json())
        # return json.dumps(parsers.to_json(), allow_nan=False, cls=MongoEncoder), 200
        return jsonify(results=parsers)


class DocumentsListByParsersListResource(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        current_user_username = current_user.split()[0]
        current_user_id = current_user.split()[1]
        parsers = models.Parser.objects(Q(owners=models.UserRef(username=current_user_username, id=current_user_id)) \
                                        | Q(editors=models.UserRef(username=current_user_username, id=current_user_id)) \
                                        | Q(viewers=models.UserRef(username=current_user_username, id=current_user_id)))
        documents = set()
        for parser in parsers:
            # parserRef = models.ParserRef(id=parser.id)#, name=parser.name)
            docs = models.Document.objects(parserRef__id=parser.id)
            if docs:
                documents |= set(docs)

        # document list create by username
        documents_by_userId = models.Document.objects(uploadBy__id=current_user_id)
        documents |= set(documents_by_userId)

        #print(len(documents))
        return jsonify(results=list(documents))


class ParserAddResource(Resource):
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


class ParserResource(Resource):
    @jwt_required
    def get(self, parserId):
        current_user = get_jwt_identity()
        current_user_username, current_user_id = current_user.split()
        parser = models.Parser.objects(id=parserId).get()
        if models.UserRef(username=current_user_username, id=current_user_id) in \
                                parser.owners+parser.editors+parser.viewers:
            return jsonify(parser)
        else:
            abort(401, description="you don't have permission.")

    @jwt_required
    def put(self, parserId):
        current_user = get_jwt_identity()  # todo need to check permission of parser
        current_user_username, current_user_id = current_user.split()
        parser_json = request.get_json()
        parser = models.Parser.objects(id=parserId).get()
        # print(parser_json.items())
        for (key, val) in parser_json.items():
            # print(key, val)
            if key in ["editors", "viewers"]: # todo add viewer
                parser[key] = [models.UserRef(username=username, id=models.User.objects(username=username).get().id) for username in val]
            elif key in ["owners"]:
                parser[key] = [models.UserRef.from_json(str(user).replace("'", "\"")) for user in val]
            elif key in ["parserRules"]:
                parser[key] = [models.ParserRule.from_json(str(parserRule).replace("'", "\"")) for parserRule in val]
            elif key in ["updated_at", "created_at", "_id"]:
                pass
            else:
                parser[key] = val
        # todo documents parseref change
        documents = models.Document.objects(parserRef__id=parserId)
        for doc in documents:
            doc.parserRef.name = parser.name
            doc.save()
        parser.save()
        return jsonify(parser)

    @jwt_required
    def delete(self, parserId):  # todo need to check permission of parser
        parser = models.Parser.objects(id=parserId)
        docs = models.Document.objects(parserRef__id=parserId)
        for doc in docs:
            doc.parserRef = None
            doc.save()
        parser.delete()
        return jsonify('deleted')


class ParserRulesResource(Resource):
    @jwt_required
    def get(self, parserId):
        current_user = get_jwt_identity()
        current_user_username, current_user_id = current_user.split()   # todo need to check permission of parser
        parser = models.Parser.objects(id=parserId).get()
        return jsonify(results=parser.parserRules)

    @jwt_required
    def post(self, parserId):
        current_user = get_jwt_identity()
        current_user_username, current_user_id = current_user.split()   # todo need to check permission of parser
        parser = models.Parser.objects(id=parserId).get()
        parserRule_json = request.get_json(force=True)
        parserRule = models.ParserRule.from_json(str(parserRule_json).replace("'", "\""))
        if parserRule.name in [i.name for i in parser.parserRules]:
            abort(409, description="parserule already exists.")
        parser.parserRules += [parserRule]
        parser.save()
        return jsonify(parser)

    @jwt_required
    def put(self, parserId):
        current_user = get_jwt_identity()
        current_user_username, current_user_id = current_user.split()  # todo need to check permission of parser
        parserRule_json = request.get_json(force=True)
        parserRule = models.ParserRule.from_json(str(parserRule_json).replace("'", "\""))
        parsers = models.Parser.objects(Q(id=parserId))  # .get()
        updated = parsers.filter(parserRules__oid=parserRule.oid).update_one(set__parserRules__S=parserRule)
        if not updated:  # push if not exist
            parser = parsers.get()
            if parserRule.name in [i.name for i in parser.parserRules]:
                abort(409, description="parserule already exists.")
            parser.parserRules += [parserRule]
            parser.save()
            #parsers.update_one(push__parserRules=parserRule)
        return jsonify(parsers)

    @jwt_required
    def delete(self, parserId):
        current_user = get_jwt_identity()
        current_user_username, current_user_id = current_user.split()  # todo need to check permission of parser
        parserRule_json = request.get_json(force=True)
        parser = models.Parser.objects(Q(id=parserId))
        updated = parser.update_one(pull__parserRules__oid=parserRule_json['oid']['$oid'])
        if updated:
            return jsonify(parser)
        else:
            return abort(410, description="parserule do not  exists.")

class UserRefResource(Resource):
    def get(self, username): # todo need jwt requitr
        user = models.User.objects(username=username).get()
        return jsonify(models.UserRef(username=username, id=user.id))

api.add_resource(PrivateResource, '/private')
api.add_resource(DocumentAddResource, '/documents/add')
api.add_resource(DocumentExtractResource, '/documents/extract/<string:documentId>')
api.add_resource(DocumentUploadResource, '/documents/upload/<string:documentId>')
api.add_resource(DocumentsListResource, '/documents/list/<string:parserId>')
api.add_resource(DocumentRecommendResource, '/documents/recommend/<string:documentId>')
api.add_resource(DocumentResource, '/documents/<string:documentId>')
api.add_resource(ParserAddResource, '/parsers/add')
api.add_resource(ParsersListResource, '/parsers/list')
api.add_resource(DocumentsListByParsersListResource, '/documents/list')
api.add_resource(ParserResource, '/parsers/<string:parserId>')
api.add_resource(ParserRulesResource, '/parserrules/<string:parserId>')
api.add_resource(UserRefResource, '/userRef/<string:username>')
api.add_resource(DocumentExtractPreviewResource, '/parserrules/extract/<string:documentId>')

def load_classification_model():
    from sklearn.neighbors.nearest_centroid import NearestCentroid
    nearestCentroid = NearestCentroid()
    parsers = models.Parser.objects()
    X_train=[]
    y_train=[]

    nearestCentroid.fit(X_train, y_train)
    return nearestCentroid

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='127.0.0.1', port=port, debug=True)

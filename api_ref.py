# from flask import Flask, request, json, Response
# from pymongo import MongoClient

# # initialized the Flask APP
# app = Flask(__name__)

# class CrudAPI:  # MongoDB Model for ToDo CRUD Implementation
#     def __init__(self, data):   # Fetchs the MongoDB, by making use of Request Body
#         self.client = MongoClient("mongodb://localhost:27017/")
#         database = data['database']
#         collection = data['collection']
#         cursor = self.client[database]
#         self.collection = cursor[collection]
#         self.data = data

#     def insert_data(self, data):    # Create - (1) explained in next section
#         new_document = data['Document']
#         response = self.collection.insert_one(new_document)
#         output = {'Status': 'Successfully Inserted',
#                   'Document_ID': str(response.inserted_id)}
#         return output

#     def read(self):                 # Read - (2) explained in next section
#         documents = self.collection.find()
#         output = [{item: data[item] for item in data if item != '_id'} for data in documents]
#         return output

#     def update_data(self):          # Update - (3) explained in next section
#         filter = self.data['Filter']
#         updated_data = {"$set": self.data['DataToBeUpdated']}
#         response = self.collection.update_one(filter, updated_data)
#         output = {'Status': 'Successfully Updated' if response.modified_count > 0 else "Nothing was updated."}
#         return output

#     def delete_data(self, data):    # Delete - (4) explained in next section
#         filter = data['Filter']
#         response = self.collection.delete_one(filter)
#         output = {'Status': 'Successfully Deleted' if response.deleted_count > 0 else "Document not found."}
#         return output

# # Achieving CRUD through API - '/crudapi'
# @app.route('/crudapi', methods=['GET'])     # Read MongoDB Document, through API and METHOD - GET
# def read_data():
#     data = request.json
#     if data is None or data == {}:
#         return Response(response=json.dumps({"Error": "Please provide connection information"}),
#                         status=400, mimetype='application/json')
#     read_obj = CrudAPI(data)
#     response = read_obj.read()
#     return Response(response=json.dumps(response), status=200,
#                     mimetype='application/json')


# @app.route('/crudapi', methods=['POST'])    # Create MongoDB Document, through API and METHOD - POST
# def create():
#     data = request.json
#     if data is None or data == {} or 'Document' not in data:
#         return Response(response=json.dumps({"Error": "Please provide connection information"}),
#                         status=400, mimetype='application/json')
#     create_obj = CrudAPI(data)
#     response = create_obj.insert_data(data)
#     return Response(response=json.dumps(response), status=200,
#                     mimetype='application/json')

# @app.route('/crudapi', methods=['PUT'])     # Update MongoDB Document, through API and METHOD - PUT
# def update():
#     data = request.json
#     if data is None or data == {} or 'Filter' not in data:
#         return Response(response=json.dumps({"Error": "Please provide connection information"}),
#                         status=400, mimetype='application/json')
#     update_obj = CrudAPI(data)
#     response = update_obj.update_data()
#     return Response(response=json.dumps(response), status=200,
#                     mimetype='application/json')


# @app.route('/crudapi', methods=['DELETE'])   # Delete MongoDB Document, through API and METHOD - DELETE
# def delete():
#     data = request.json
#     if data is None or data == {} or 'Filter' not in data:
#         return Response(response=json.dumps({"Error": "Please provide connection information"}),
#                         status=400, mimetype='application/json')
#     delete_obj = CrudAPI(data)
#     response = delete_obj.delete_data(data)
#     return Response(response=json.dumps(response), status=200,
#                     mimetype='application/json')

# if __name__ == '__main__':
#     app.run(debug=True, port=5000)

import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/todo_db"

db = MongoEngine()
db.init_app(app)

class User(db.Document):
    name = db.StringField()
    email = db.StringField()
    def to_json(self):
        return {"name": self.name,
                "email": self.email}

@app.route('/', methods=['GET'])
def query_records():
    name = request.args.get('name')
    user = User.objects(name=name).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        return jsonify(user.to_json())

@app.route('/', methods=['PUT'])
def create_record():
    record = request.json
    user = User(name=record['name'],
                email=record['email'])
    user.save()
    return jsonify(user.to_json())

@app.route('/', methods=['POST'])
def update_record():
    record = request.json
    user = User.objects(name=record['name']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.update(email=record['email'])
    return jsonify(user.to_json())

@app.route('/', methods=['DELETE'])
def delete_record():
    record = json.loads(request.data)
    user = User.objects(name=record['name']).first()
    if not user:
        return jsonify({'error': 'data not found'})
    else:
        user.delete()
    return jsonify(user.to_json())

if __name__ == "__main__":
    app.run(debug=True)
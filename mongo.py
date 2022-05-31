
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from pymongo import MongoClient
from werkzeug.security import check_password_hash, generate_password_hash
from token_generator import generate_token

import ssl


    
app = Flask(__name__)
# This would usually come from your config file

app.config["MONGODB_SETTINGS"] = { 
                                  "host" : "mongodb+srv://joseph:Horladapor2012@cluster-test.hnakk.mongodb.net/test?retryWrites=true"
                                  }
db = MongoEngine(app)
try:
   _create_unverified_https_context = ssl._create_unverified_context
   db.connect(db = 'test', host="mongodb+srv://joseph:Horladapor2012@cluster-test.hnakk.mongodb.net/test?retryWrites=true")
except :
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context
    


class User(db.Document):
    first_name = db.StringField()
    last_name = db.StringField()
    email = db.StringField()
    password = db.StringField(required=True)
    
    
    def to_json(self):
        return {"name": " ".join([self.first_name,self.last_name]),
                "email": self.email,
                "message": 'Successfully created'}

@app.route('/register', methods=['POST'])
def register():
    details = request.json
  
    pwd = generate_password_hash(details['password'], 'sha256')
 
 
    user = User(
                        first_name= details['first_name'],
                        last_name = details['last_name'],
                        email = details['email'],
                        password = pwd
                        )
    user.save()
    return user.to_json()


if __name__ == '__main__':
    app.run()
    db.disconnect()

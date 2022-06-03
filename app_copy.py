import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from werkzeug.security import check_password_hash, generate_password_hash
from token_generator import generate_token
from encoder import encode_data,decode_data

import os

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = { #'connect':False,
                                  "host" : f"mongodb+srv://joseph:Horladapor2012@cluster-test.hnakk.mongodb.net/test?retryWrites=true&ssl=true&tlsAllowInvalidCertificates=true"
                                  }
                               
db = MongoEngine()
db.init_app(app)



class User(db.Document):
    
    """
            This document stores the user records and keeps them for reference
    
    """
    first_name = db.StringField()
    last_name = db.StringField()
    email = db.StringField()
    password = db.StringField(required=True)
    secret_key = db.StringField()
    
    
    def to_json(self):
        return {"name": " ".join([self.first_name,self.last_name]),
                "email": self.email,
                "message": 'Account Successfully created',
                "login condition": "Add the secret key to your authorization header to login. Mode 'Bearer <secret_key>'"}


class Login_status(db.Document):
    
    """
        This Documents keeps record of the login token given to a user that logs in
        It saves the email and token, so that the user can use his token to create, view templates
        
    """
    
    email = db.StringField()
    token = db.StringField()
        
class Template(db.Document):
    """
        Stores all the templates posted by users
    """
    email =  db.StringField()
    template_name = db.StringField()
    subject= db.StringField()
    body = db.StringField()
    
    def to_json(self):
        return        {"name": self.template_name,
                        "subject": self.subject,
                        'body':self.body
                        }
                    
        
# the routes
        
@app.route('/register', methods=['POST'])
def register():
    """
        This function registers new users and saves their details in the User document
        
    """
    details = request.json
    pwd = generate_password_hash(details['password'], 'sha256')
 
 
    user = User(
                        first_name= details['first_name'],
                        last_name = details['last_name'],
                        email = details['email'],
                        password = pwd,
                        secret_key = details['secret_key']
                        )
    user.save()
    return user.to_json()



@app.route('/login', methods=['POST'])
def login():
    login = request.json   # loads the request data
    user = User.objects(email=login['email']).first()   
    if not user and check_password_hash(user.password, login['password']):   # # checks if email exists and password is correct
        return jsonify({
                        'error': 'Kindly register or retype password',
                        })
    
    else:
        SECRET_KEY = request.headers['Authorization'].split(' ')[1][:-1]   # carries te secret key from the header 
        token = encode_data(json_data= login ,secret = SECRET_KEY)          # encoding the secret key
        login = Login_status(email =user.email, token=token )               # saving the token generated to be accessed later
        login.save()
        return jsonify(
                        {
                            'message': 'Login Successful, kindly save token, expires after 5 mins',
                            'token' : f'{token}'
                        }
                       )



@app.route('/template', methods=['POST', 'GET'])
def templates():
    token = request.headers['Authorization'].split(' ')[1][:-1]             # to check for token
    
    login = Login_status.objects(token=token).first()
    if login:                                                                # checks if token exists'      
     # checks if the token is valid, returns true or false and e==
        auth, valid = decode_data(token, User.objects(email=login.email).first().secret_key)
        if valid: 
            if request.method=='POST':                                      # if user posts a template      
                temps = request.json
                new_template = Template( email = login.email,
                                                template_name=temps['template_name'],
                                                subject = temps['subject'],
                                                body = temps['body']
                                                )
                new_template.save()
                return jsonify({
                                'message': 'template saved successfully'
                                })
                
            else:
                templates = Template.objects(email=login.email).all()       # to display all templates by user 
                list_of_templates = {str(index+1):temp.to_json() for index,temp in enumerate(templates)}              
                return jsonify(body=list_of_templates)
            
        else:
            return jsonify({
                            'message':f'{auth}, No authorisation, Kindly /login again',
                           })
    else:
        return jsonify({'message':'Token doesnt exist'})
    
  
        
@app.route('/template/<template_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_template(template_id):
    """
        This allows user to update, delete and fetch a template.
    """

    token = request.headers['Authorization'].split(' ')[1][:-1]
    # to check for token
    login= Login_status.objects(token=token).first()
    if login:    
        auth, valid = decode_data(token, User.objects(email=login.email).first().secret_key )    
        message = ''
        if valid: 
            temps = request.json
            selected_template = Template.objects(email=login.email)[int(template_id)]
            if request.method=='PUT':            
                selected_template.update(   template_name=temps['template_name'],
                                                subject = temps['subject'],
                                                body = temps['body']
                                            ) 
                message = {
                            "message":"Template updated successfully"
                            }
                
            elif request.method =='GET':
                message = selected_template.to_json()
            else:
                selected_template.delete()
                message = {
                            'message':'Deleted successfully'
                            }
        else:
            message = {
                        'message':f'{auth}, Kindly login again'
                        }
    else:
        message = {"No authorisation, token doesn't exist"}
            
    return jsonify(message)
    

if __name__ == "__main__":
    app.run(debug=True)
    db.disconnect()
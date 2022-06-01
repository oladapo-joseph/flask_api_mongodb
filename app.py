import json
from flask import Flask, request, jsonify
from flask_mongoengine import MongoEngine
from werkzeug.security import check_password_hash, generate_password_hash
from token_generator import generate_token
# import logger
import os

app = Flask(__name__)
app.config["MONGODB_SETTINGS"] = { #'connect':False,
                                  "host" : f"mongodb+srv://joseph:{os.environ.get('password')}@cluster-test.hnakk.mongodb.net/test?retryWrites=true&ssl=true&tlsAllowInvalidCertificates=true"
                                  }
                               
db = MongoEngine()
db.init_app(app)



class User(db.Document):
    first_name = db.StringField()
    last_name = db.StringField()
    email = db.StringField()
    password = db.StringField(required=True)
    
    
    def to_json(self):
        return {"name": " ".join([self.first_name,self.last_name]),
                "email": self.email,
                "message": 'Successfully created'}


class Login_status(db.Document):
    
    """
        This Documents keeps record of the login token given to a user that logs in
        It saves the email and token, so that the user can use his token to create, view templates
        
    """
    email = db.StringField()
    token = db.StringField()
        
class Template(db.Document):
    """
        Stores all the templates
    """
    email =  db.StringField()
    template_name = db.StringField()
    subject= db.StringField()
    body = db.StringField()
    
    def to_json(self):
        return        {"name": self.template_name,
                        "subject": self.subject,
                        'email':self.email
                        }
                    
        
# the routes
        
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


@app.route('/login', methods=['POST'])
def login():
    login = request.json
    user = User.objects(email=login['email']).first()
    
    if not user and check_password_hash(user.password, login['password']):
        return jsonify({
                        'error': 'Kindly register or retype password',
                        })
    
    else:
        # check first if user token exists
        log = Login_status.objects(email=login['email']).first()
        token = generate_token()
        if not log :        # new user login
            login_data = Login_status(email=login['email'], token= token)
            login_data.save()
        else:
            log.update(token = token)
        return jsonify(
                        {
                            'message': 'Login Successful',
                            'token' : f'Kindly save token: {token}'
                        }
                       )



@app.route('/template', methods=['POST', 'GET'])
def templates():
    token = request.headers['Authorization'].split(' ')[1][:-1]
    # to check for token
    auth = Login_status.objects(token=token).first()
    if auth: 
        if request.method=='POST':            
            temps = request.json
            new_template = Template( email = auth.email,
                                            template_name=temps['template_name'],
                                            subject = temps['subject'],
                                            body = temps['body']
                                            )
            new_template.save()
            return jsonify({'message': 'template saved successfully'})
        else:
            templates = Template.objects(email=auth.email).all()
            list_of_templates = {str(index+1):temp.to_json() for index,temp in enumerate(templates)}              
            return jsonify(body=list_of_templates)
    else:
        return jsonify({
                    'message':'no authorisation',
                    'token_sent': f'{token}',
                #    ? 'token' : f'{auth.token}'
        })
        
        
@app.route('/template/<template_id>', methods=['GET', 'PUT', 'DELETE'])
def edit_template(template_id):
    token = request.headers['Authorization'].split(' ')[1][:-1]
    # to check for token
    auth = Login_status.objects(token=token).first()
    message = ''
    if auth: 
        temps = request.json
        selected_template = Template.objects(email=auth.email)[int(template_id)]
        if request.method=='PUT':            
            selected_template.update(   template_name=temps['template_name'],
                                            subject = temps['subject'],
                                            body = temps['body']
                                        ) 
            message = {"message":"Template updated successfully"}
        elif request.method =='GET':
            message = selected_template.to_json()
        else:
            selected_template.delete()
            message = {'message':'Deleted successfully'}
    else:
        message = {
                    'message':'no authorisation'
                    }
    
    return jsonify(message)
    

if __name__ == "__main__":
    app.run(debug=True)
    db.disconnect()
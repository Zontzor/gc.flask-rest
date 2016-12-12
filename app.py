#!flask/bin/python
from flask_sqlalchemy import SQLAlchemy  
from flask import Flask, jsonify, request, abort, make_response

app = Flask(__name__)

# MySQL configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://alex:Cany0n@localhost/glucose_coach'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Instantiate db object
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('u_username', db.String(30))
    password = db.Column('u_password', db.String(30))
    email = db.Column('u_email', db.String(30))
    firstname = db.Column('u_firstname', db.String(30))
    weight = db.Column('u_weight', db.Integer)
    height = db.Column('u_height', db.Integer)
    date_created = db.Column('u_date_created', db.Date)
    profile_image_path = db.Column('u_profile_image_path', db.String(100))
    
    # Users constructor
    def __init__(self, id, username, password, email, firstname, weight, height, date_created, profile_image_path):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.firstname = firstname
        self.weight = weight
        self.height = height
        self.date_created = date_created
        self.profile_image_path = profile_image_path
        
    def __repr__(self):
        return '<Users (%s, %s) >' % (self.username, self.firstname)
    
    def serialize(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'password' : self.password,
            'email' : self.email,
            'firstname' : self.firstname,
            'weight' : self.weight,
            'height' : self.height,
            'date_created' : self.date_created,
            'profile_image_path' : self.profile_image_path
        }

#############
# Index
############
@app.route("/glucose_coach/api/v1.0/")
def index():  
    return """
Available API endpoints:

GET /users - List all users

"""  
    
#############
# User
############
@app.route('/glucose_coach/api/v1.0/users', methods=['GET'])
def get_users():
    data = Users.query.all() #fetch all users on the table
    data_all = []
    for user in data:
        data_all.append(user.serialize()) #prepare visual data
    
    return jsonify(users=data_all)
    
@app.route('/glucose_coach/api/v1.0/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = Users.query.filter_by(id=user_id).first()
    
    if user is None:
        abort(404)
        
    result = user.serialize()
    return jsonify(result)
    
##################
# Blood glucose
##################

#############
# Error
############
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 500)

if __name__ == "__main__":  
    app.run(debug = True)
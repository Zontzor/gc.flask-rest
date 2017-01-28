#!flask/bin/python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, abort, make_response

#import dateutil.parser

app = Flask(__name__)

# MySQL configurations
app.config['SQLALCHEMY_DATABASE_URI'] = ("mysql+mysqldb://alex:Cany0n@" + 
"localhost/glucose_coach")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Instantiate db object
db = SQLAlchemy(app)

from resources.user import User
from resources.bgreading import BGReading

#############
# Index
############
@app.route("/glucose_coach/api/v1.0")
def index():  
    return """
Available API endpoints:

GET /users - List all users
GET /users/<username> - List a user
POST /users - Add a user
PUT /users - Update a users info
DELETE /users/<username> - Delete a user

GET /users/<username>/bgreadings - Get a users blood glucose results
POST /users/<username>/bgreadings - Add a user blood glucose result
"""  
    
#############
# User
############
@app.route('/glucose_coach/api/v1.0/users', methods=['GET'])
def get_users():
    data = User.query.all() #fetch all users on the table
    data_all = []
    for user in data:
        data_all.append(user.serialize()) #prepare visual data
    
    return jsonify(users=data_all)
    
@app.route('/glucose_coach/api/v1.0/users/<string:user_name>', methods=['GET'])
def get_user(user_name):
    user = User.query.filter_by(username=user_name).first()
    
    if user is None:
        abort(404)
        
    return jsonify(user.serialize())

@app.route('/glucose_coach/api/v1.0/users', methods=['POST'])
def create_user():
    username = request.get_json()['username']
    password = request.get_json()['password']
    email = request.get_json()['email']
    firstname = request.get_json()['firstname']
    
    user = User(username = username, password = password, email = email, 
    firstname = firstname)
    
    curr_session = db.session #open database session
    try:
        curr_session.add(user) #add prepared statment to opened session
        curr_session.commit() #commit changes
    except:
        curr_session.rollback()
        curr_session.flush() 
        print("Add user error")
    
    return jsonify(user.serialize())
    
@app.route('/glucose_coach/api/v1.0/users/<string:user_name>', methods=['PUT']) 
def update_user(user_name):
    user = User.query.filter_by(username=user_name).first()
    
    curr_session = db.session 
    try:
        if 'username' in request.json:
            user.username = request.get_json()['username'] 
        if 'password' in request.json:
            user.password = request.get_json()['password'] 
        if 'email' in request.json:
            user.email = request.get_json()['email'] 
        if 'firstname' in request.json:
            user.firstname = request.get_json()['firstname'] 
        if 'weight' in request.json:
            user.weight = request.get_json()['weight']
        if 'height' in request.json:
            user.username = request.get_json()['height']
        if 'date_created' in request.json:
            user.date_created = request.get_json()['date_created']
        if 'profile_image_path' in request.json:
            user.profile_image_path = request.get_json()['profile_image_path']
        
        curr_session.commit()
    except:
        curr_session.rollback()
        curr_session.flush()

    return jsonify(user.serialize())
    
@app.route('/glucose_coach/api/v1.0/users/<string:user_name>', 
methods=['DELETE'])
def delete_user(user_name):
    curr_session = db.session

    User.query.filter_by(username=user_name).delete() 
    curr_session.commit()

    return jsonify({'result': True}) 
    
##################
# Blood glucose
##################
@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/bgreadings', 
methods=['GET'])
def get_user_bgreadings(user_name):
    user = User.query.filter_by(username=user_name).first()
    data = BGReading.query.filter_by(username=user_name).all()
    data_all = []
    
    for bgreading in data:
        data_all.append(bgreading.serialize()) 
    
    if user is None:
        abort(404)
        
    return jsonify(bgreadings=data_all)
    
@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/bgreadings', 
methods=['POST'])
def add_bg(user_name):
    username = request.get_json()['username']
    bg_value = request.get_json()['bg_value']
    bg_timestamp = request.get_json()['bg_timestamp']
    
    bg_reading = BGReading(username = username, bg_value = bg_value, 
    bg_timestamp = bg_timestamp)
    
    user = User.query.filter_by(username=user_name).first()
    
    if user is None:
        abort(404)
    
    curr_session = db.session #open database session
    try:
        curr_session.add(bg_reading) #add prepared statment to opened session
        curr_session.commit() #commit changes
    except:
        curr_session.rollback()
        curr_session.flush() 
        print("Add bgreading error")
    
    return jsonify(bg_reading.serialize())

"""@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/bgreadings/<string:datestamp>', 
methods=['GET'])
def get_user_bgreadings_day(user_name, datestamp):
    user = User.query.filter_by(username=user_name).first()
    data = BGReading.query.filter_by(username=user_name).all()
    data_all = []
    
    # Parse date from each bg reading and match to users requested date
    for bgreading in data:
        date = dateutil.parser.parse(str(bgreading.bg_timestamp)).date()
        if (datestamp == str(date)):
            data_all.append(bgreading.serialize()) 
    
    if user is None:
        abort(404)
        
    return jsonify(bgreadings=data_all)"""


#############
# Error
############
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(500)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 500)
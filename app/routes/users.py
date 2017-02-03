from app import app, db, auth
from flask import Flask, jsonify, request, abort, make_response 
from ..resources.user import User

@app.route('/glucose_coach/api/v1.0/users', methods=['GET'])
def read_users():
    data = User.query.all() #fetch all users on the table
    data_all = []
    for user in data:
        data_all.append(user.serialize()) #prepare visual data
    
    return jsonify(users=data_all)
    
@app.route('/glucose_coach/api/v1.0/users/<string:user_name>', methods=['GET'])
@auth.login_required
def read_user(user_name):
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
    
    if username is None or password is None:
        abort(400) # missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400) # existing user
        
    user = User(username = username, email = email, firstname = firstname)
        
    user.hash_password(password)
    
    print(user.username + ', ' + user.password_hash + ', ' + user.email + ', ' + user.firstname)
    
    curr_session = db.session #open database session
    try:
        curr_session.add(user) #add prepared statment to opened session
        curr_session.commit() #commit changes
    except:
        curr_session.rollback()
        curr_session.flush() 
        abort(400)
    
    return jsonify(user.serialize())
    
@app.route('/glucose_coach/api/v1.0/users/<string:user_name>', methods=['PUT']) 
def update_user(user_name):
    user = User.query.filter_by(username=user_name).first()
    
    if user is None:
        abort(404)
    
    curr_session = db.session 
    try:
        if 'username' in request.json:
            user.username = request.get_json()['username'] 
        if 'password' in request.json:
            user.hash_password(request.get_json()['username'])
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
    
"""
 28/1/17 - Not using for the moment as there are dependencies on users

@app.route('/glucose_coach/api/v1.0/users/<string:user_name>', 
methods=['DELETE'])
def delete_user(user_name):
    curr_session = db.session
    
    user = User.query.filter_by(username=user_name).first()
    if user is None:
        abort(404)

    User.query.filter_by(username="Test").delete() 
    
    curr_session.commit()

    return jsonify({'result': True}) """
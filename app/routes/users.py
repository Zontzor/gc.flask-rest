"""
    Author: Alex Kiernan

    Desc: Users routes
"""
from app import app, db, auth
from flask import jsonify, request, abort
from ..resources.user import User
import datetime


@app.route('/glucose_coach/api/v1.0/users/usernames/<string:user_name>', methods=['GET'])
def read_username(user_name):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    return jsonify(user.username)


@app.route('/glucose_coach/api/v1.0/users', methods=['GET'])
@auth.login_required
def read_users():
    data = User.query.all()  # Fetch all users on the table
    data_all = []
    for user in data:
        data_all.append(user.serialize())  # Prepare visual data

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

    date_created = datetime.datetime.now()

    if username is None or password is None:
        abort(400)  # Missing arguments
    if User.query.filter_by(username = username).first() is not None:
        abort(400)  # Existing user

    user = User(username = username, email = email)

    user.hash_password(password)

    user.date_created = date_created

    user.last_sync_date = '2000-01-01 00:00:00'

    curr_session = db.session
    try:
        curr_session.add(user)
        curr_session.commit()
    except:
        curr_session.rollback()
        curr_session.flush()
        abort(400)

    return jsonify(user.serialize())


@app.route('/glucose_coach/api/v1.0/users/<string:user_name>', methods=['PUT'])
@auth.login_required
def update_user(user_name):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    curr_session = db.session
    try:
        if 'username' in request.json:
            user.username = request.get_json()['username']
        if 'password' in request.json:
            user.hash_password(request.get_json()['password'])
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
        print("Error")
        curr_session.rollback()
        curr_session.flush()

    return jsonify(user.serialize())

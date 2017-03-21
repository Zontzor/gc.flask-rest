"""
    Author: Alex Kiernan

    Desc: Food logs routes
"""
from app import app, db, auth
from flask import jsonify, request, abort
from ..resources.user import User
from ..resources.food_log import FoodLog


@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/foodlogs', methods=['GET'])
@auth.login_required
def read_all_foodlogs(user_name):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    data = FoodLog.query.filter_by(user_id=user.id).all()
    data_all = []

    for food_log in data:
        data_all.append(food_log.serialize())

    return jsonify(data_all)


@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/foodlogs/<int:fl_id>', methods=['GET'])
@auth.login_required
def read_food_log(user_name, fl_id):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    food_log = FoodLog.query.filter_by(id=fl_id).first()

    if food_log is None:
        abort(404)

    return jsonify(food_log.serialize())


@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/foodlogs', methods=['POST'])
def create_food_log(user_name):
    food_id = request.get_json()['food_id']
    fl_quantity = request.get_json()['fl_quantity']
    fl_timestamp = request.get_json()['fl_timestamp']

    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    food_log = FoodLog(user_id=user.id, food_id=food_id, fl_quantity=fl_quantity, fl_timestamp=fl_timestamp)

    curr_session = db.session
    try:
        curr_session.add(food_log)
        curr_session.commit()
    except:
        curr_session.rollback()
        curr_session.flush()

    return jsonify(food_log.serialize())


@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/foodlogs/<int:fl_id>', methods=['PUT'])
@auth.login_required
def update_food_log(user_name, fl_id):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    food_log = FoodLog.query.filter_by(id=fl_id).first()

    if food_log is None:
        abort(404)

    curr_session = db.session
    try:
        if 'food_id' in request.json:
            food_log.food_id = request.get_json()['food_id']
        if 'fl_quantity' in request.json:
            food_log.fl_quantity = request.get_json()['fl_quantity']
        if 'fl_timestamp' in request.json:
            food_log.fl_timestamp = request.get_json()['fl_timestamp']

        curr_session.commit()
    except:
        curr_session.rollback()
        curr_session.flush()

    return jsonify(food_log.serialize())

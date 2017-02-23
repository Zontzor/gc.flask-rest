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

    return jsonify(food_logs=data_all)
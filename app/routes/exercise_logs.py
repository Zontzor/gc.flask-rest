from app import app, db, auth
from flask import jsonify, request, abort
from ..resources.user import User
from ..resources.exercise_log import ExerciseLog

@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/exerciselogs', methods=['GET'])
@auth.login_required
def read_all_exerciselogs(user_name):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    data = ExerciseLog.query.filter_by(user_id=user.id).all()
    data_all = []

    for exercise_log in data:
        data_all.append(exercise_log.serialize())

    return jsonify(exercise_logs=data_all)
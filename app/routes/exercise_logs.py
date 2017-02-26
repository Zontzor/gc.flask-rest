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


@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/exerciselogs/<int:el_id>', methods=['GET'])
@auth.login_required
def read_els(user_name, el_id):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    exercise_log = ExerciseLog.query.filter_by(id=el_id).first()

    if exercise_log is None:
        abort(404)

    return jsonify(exercise_log.serialize())


@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/exerciselogs', methods=['POST'])
@auth.login_required
def create_el(user_name):
    exercise_id = request.get_json()['exercise_id']
    el_duration = request.get_json()['el_duration']
    el_timestamp = request.get_json()['el_timestamp']

    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    exercise_log = ExerciseLog(user_id=user.id, exercise_id=exercise_id, el_duration=el_duration,
                               el_timestamp=el_timestamp)

    curr_session = db.session  # open database session
    try:
        curr_session.add(exercise_log)  # add prepared statment to opened session
        curr_session.commit()  # commit changes
    except:
        curr_session.rollback()
        curr_session.flush()

    return jsonify(exercise_log.serialize())


@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/exerciselogs/<int:el_id>', methods=['PUT'])
@auth.login_required
def update_el(user_name, el_id):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    exercise_log = ExerciseLog.query.filter_by(id=el_id).first()

    if exercise_log is None:
        abort(404)

    curr_session = db.session
    try:
        if 'exercise_id' in request.json:
            exercise_log.exercise_id = request.get_json()['exercise_id']
        if 'el_duration' in request.json:
            exercise_log.el_duration = request.get_json()['el_duration']
        if 'bg_timestamp' in request.json:
            exercise_log.el_timestamp = request.get_json()['el_timestamp']

        curr_session.commit()
    except:
        curr_session.rollback()
        curr_session.flush()

    return jsonify(exercise_log.serialize())
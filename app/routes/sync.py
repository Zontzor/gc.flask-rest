from app import app, db, auth
from flask import jsonify, request, abort
from ..resources.user import User


@app.route('/glucose_coach/api/v1.0/sync/<string:user_name>', methods=['GET'])
@auth.login_required
def read_last_sync_date(user_name):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    return jsonify(user.last_sync_serialize())


@app.route('/glucose_coach/api/v1.0/sync/<string:user_name>', methods=['POST'])
@auth.login_required
def set_last_sync_date(user_name):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    curr_session = db.session
    try:
        if 'last_sync_date' in request.json:
            user.last_sync_date = request.get_json()['last_sync_date']

        curr_session.commit()
    except:
        print("Error")
        curr_session.rollback()
        curr_session.flush()

    return jsonify(user.last_sync_date)

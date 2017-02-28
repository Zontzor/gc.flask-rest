from app import app, db, auth
from flask import jsonify, request, abort
from ..resources.user import User
from ..resources.fact import Fact


@app.route('/glucose_coach/api/v1.0/facts/<string:user_name>', methods=['GET'])
def read_fact(user_name):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    fact = Fact.query.filter_by(user_id=user.id).first()

    return jsonify(fact.serialize())
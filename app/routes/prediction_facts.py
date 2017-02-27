from app import app, db, auth
from flask import jsonify, request, abort
from ..resources.user import User
from ..resources.prediction_fact import PredictionFact


@app.route('/glucose_coach/api/v1.0/predictionfacts/<string:user_name>', methods=['GET'])
@auth.login_required
def read_prediction_fact(user_name):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    prediction_fact = PredictionFact.query.filter_by(user_id=user.id).first()

    return jsonify(prediction_fact.fact_serialize())
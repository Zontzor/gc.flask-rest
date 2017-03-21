"""
    Author: Alex Kiernan

    Desc: Foods routes
"""
from app import app, auth
from flask import jsonify
from ..resources.food import Food


@app.route('/glucose_coach/api/v1.0/foods', methods=['GET'])
@auth.login_required
def read_all_foods():
    data = Food.query.all()
    data_all = []

    for food in data:
        data_all.append(food.serialize())

    return jsonify(data_all)

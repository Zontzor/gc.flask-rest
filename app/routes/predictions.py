from app import app, db
import os.path
from flask import Flask, request, jsonify, abort
from ..resources.user import User
from ..resources.fact import Fact
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib

# Load dir
model_directory = 'storage/models'
model_prefix = '/model_user_'
model_ext = '.pkl'


def get_input_from_json(input_json):
    return np.array(
        [[
            input_json['pf_time_of_day'],
            input_json['bg_value'],
            input_json['food_value'],
            input_json['exercise_value']
        ]]
    )


@app.route('/glucose_coach/api/v1.0/predict/<string:user_name>', methods=['POST'])
def predict(user_name):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    model_file_name = model_directory + model_prefix + str(user.id) + model_ext

    if not os.path.exists(model_file_name):
        model_file_name = model_directory + '/default_model' + model_ext

    clf = joblib.load(model_file_name)

    X = get_input_from_json(request.json)

    insulin_prediction = round(clf.predict(X)[0] * 2) / 2

    return jsonify(insulin_prediction)


@app.route('/glucose_coach/api/v1.0/train/<string:user_name>', methods=['GET'])
def train(user_name):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    data = Fact.query.filter_by(user_id=user.id).all()
    data_all = []

    for prediction_fact in data:
        data_all.append(prediction_fact.fact_serialize())

    # Split-out validation dataset
    dataset = pd.DataFrame(data_all)
    dataset = dataset[['pf_time_of_day', 'bg_value', 'food_value', 'exercise_value', 'ins_value']]

    x = dataset.values[:,0:4]
    y = dataset.values[:,4]
    validation_size = 0.20
    seed = 7
    x_train, x_validation, y_train, y_validation = model_selection.train_test_split(x, y, test_size=validation_size,
                                                                                    random_state=seed)

    lr = LinearRegression()
    lr.fit(x_train, y_train)
    predictions = lr.predict(x_validation)
    print(predictions)

    model_file_name = model_directory + model_prefix + str(user.id) + model_ext
    joblib.dump(lr, model_file_name)

    return 'Success'

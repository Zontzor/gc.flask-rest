"""
    Author: Alex Kiernan

    Desc: Routes that handle prediction generations and responses
"""
from app import app, auth
import os.path
from flask import request, jsonify, abort
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


# Generates a prediction for the user based on data passed
@app.route('/glucose_coach/api/v1.0/predict/<string:user_name>', methods=['POST'])
@auth.login_required
def predict(user_name):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    # Load the users model
    model_file_name = model_directory + model_prefix + str(user.id) + model_ext

    # If the user does not have a model, choose the default model
    if not os.path.exists(model_file_name):
        model_file_name = model_directory + '/default_model' + model_ext

    clf = joblib.load(model_file_name)

    # Get the insulin prediciton
    X = get_input_from_json(request.json)

    insulin_prediction = round(clf.predict(X)[0] * 2) / 2

    if insulin_prediction < 0:
        insulin_prediction = 0

    return jsonify(insulin_prediction)


# Generates a users model based on the data contained in their fact table
@app.route('/glucose_coach/api/v1.0/train/<string:user_name>', methods=['GET'])
@auth.login_required
def train(user_name):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    # Get all the users facts that offer good data for training
    data = Fact.query.filter_by(user_id=user.id).filter(Fact.bg_value != 0).all()

    if len(data) < 20:
        abort(404)

    data_all = []

    for prediction_fact in data:
        data_all.append(prediction_fact.fact_serialize())

    # Split-out validation dataset
    dataset = pd.DataFrame(data_all)
    dataset = dataset[['timestamp', 'bg_value', 'carbs', 'exercise', 'insulin_dosage']]

    # Choose the base and target columns
    x = dataset.values[:,0:4]
    y = dataset.values[:,4]
    validation_size = 0.20
    seed = 7
    x_train, x_validation, y_train, y_validation = model_selection.train_test_split(x, y, test_size=validation_size,
                                                                                    random_state=seed)

    # Use linear regression to generate the data
    lr = LinearRegression()
    lr.fit(x_train, y_train)
    predictions = lr.predict(x_validation)
    print(predictions)

    # Store the model named with the users id
    model_file_name = model_directory + model_prefix + str(user.id) + model_ext
    joblib.dump(lr, model_file_name)

    return 'Success'

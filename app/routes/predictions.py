from app import app, db
from flask import Flask, request, jsonify, abort
from ..resources.user import User
from ..resources.bgreading import BGReading
import pandas as pd
import numpy as np
from sklearn import model_selection
from sklearn.linear_model import LinearRegression
from sklearn.externals import joblib

# Load dir
model_directory = 'storage/models'
model_prefix = '/model_user_'
model_ext = '.pkl'

dataset = pd.read_csv("blood-glucose-results.csv", header = 0)

def get_input_from_json(input_json):
    return np.array(
        [[
            input_json['timestamp'],
            input_json['bg_value'],
            input_json['carbs'],
            input_json['exercise']
        ]]
    )

@app.route('/glucose_coach/api/v1.0/predict/<string:user_name>', methods=['POST'])
def predict(user_name):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    model_file_name = model_directory + model_prefix + str(user.id) + model_ext
    clf = joblib.load(model_file_name)

    X = get_input_from_json(request.json)

    predicition = clf.predict(X)[0]

    return jsonify(predicition)

@app.route('/glucose_coach/api/v1.0/train/<string:user_name>', methods=['GET'])
def train(user_name):
    user = User.query.filter_by(username=user_name).first()

    if user is None:
        abort(404)

    bg_readings = BGReading.query.filter_by(user_id=user.id).all()

    # Split-out validation dataset
    array = dataset.values
    x = array[:, 0:4]
    y = array[:, 4]
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
#!flask/bin/python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)

# Load config settings
app.config.from_object('config')
    
# Instantiate db object
db = SQLAlchemy(app)

auth = HTTPBasicAuth()

import callbacks.authentication

#############
# Routes
############
import routes.index
import routes.users
import routes.bgreadings
import routes.insdosages
import routes.food_logs
import routes.exercise_logs
import routes.foods
import routes.exercises
import routes.facts
import routes.predictions
import routes.sync
import routes.token
import routes.errors

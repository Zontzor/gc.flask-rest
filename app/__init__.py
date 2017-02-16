#!flask/bin/python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_httpauth import HTTPBasicAuth
import os.path

app = Flask(__name__)

# Load config settings
app.config.from_object('config')
    
# Instantiate db object
db = SQLAlchemy(app)

auth = HTTPBasicAuth()

# MySQL configurations
app.config.from_object('config')

import callbacks.authentication

from resources.user import User
from resources.bgreading import BGReading
from resources.insdosage import InsDosage

#############
# Routes
############
import routes.index
import routes.users
import routes.bgreadings
import routes.insdosages
import routes.token
import routes.errors

#!flask/bin/python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_httpauth import HTTPBasicAuth

#import dateutil.parser

app = Flask(__name__)

auth = HTTPBasicAuth()

# MySQL configurations
app.config['SQLALCHEMY_DATABASE_URI'] = ("mysql+mysqldb://alex:Cany0n@" + 
"localhost/glucose_coach")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'

# Instantiate db object
db = SQLAlchemy(app)

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

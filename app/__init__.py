#!flask/bin/python
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, abort, make_response

#import dateutil.parser

app = Flask(__name__)

# MySQL configurations
app.config['SQLALCHEMY_DATABASE_URI'] = ("mysql+mysqldb://alex:Cany0n@" + 
"localhost/glucose_coach")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Instantiate db object
db = SQLAlchemy(app)

from resources.user import User
from resources.bgreading import BGReading
    
#############
# Routes
############
import routes.index
import routes.users
import routes.bgreadings
import routes.errors

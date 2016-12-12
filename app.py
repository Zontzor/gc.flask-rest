#!flask/bin/python
from flask_sqlalchemy import SQLAlchemy  
from flask import Flask, jsonify, request

app = Flask(__name__)

# MySQL configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://alex:Cany0n@localhost/glucose_coach'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Instantiate db object
db = SQLAlchemy(app)

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('u_username', db.Unicode)
    password = db.Column('u_password', db.Unicode)
    email = db.Column('u_email', db.Unicode)
    firstname = db.Column('u_firstname', db.Unicode)
    
    # Users constructor
    def __init__(self, id, username, password, email, firstname):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.firstname = firstname
        
    def __repr__(self):
        return '<Users (%s, %s) >' % (self.username, self.firstname)

@app.route("/")
def hello():  
    return "Welcome to Glucose Coach API"
    
@app.route('/users', methods=['GET'])
def get_users():
    data = Users.query.all() #fetch all products on the table
    data_all = []
    for user in data:
        data_all.append([user.id, user.username, user.email]) #prepare visual data

    return jsonify(users=data_all)

if __name__ == "__main__":  
    app.run()
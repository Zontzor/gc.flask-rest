from app import app, db
from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('u_username', db.String(30))
    password_hash = db.Column('u_password_hash', db.String(256))
    email = db.Column('u_email', db.String(30))
    firstname = db.Column('u_firstname', db.String(30))
    weight = db.Column('u_weight', db.Float)
    height = db.Column('u_height', db.Integer)
    date_created = db.Column('u_date_created', db.Date)
    profile_image_path = db.Column('u_profile_image_path', db.String(100))
    
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def serialize(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'email' : self.email,
            'firstname' : self.firstname,
            'weight' : self.weight,
            'height' : self.height,
            'date_created' : self.date_created,
            'profile_image_path' : self.profile_image_path,
            'password_hash' : self.password_hash,
        }
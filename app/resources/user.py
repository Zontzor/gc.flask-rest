from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('u_username', db.String(30))
    password = db.Column('u_password', db.String(30))
    email = db.Column('u_email', db.String(30))
    firstname = db.Column('u_firstname', db.String(30))
    weight = db.Column('u_weight', db.Float)
    height = db.Column('u_height', db.Integer)
    date_created = db.Column('u_date_created', db.Date)
    profile_image_path = db.Column('u_profile_image_path', db.String(100))
    
    def serialize(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'password' : self.password,
            'email' : self.email,
            'firstname' : self.firstname,
            'weight' : self.weight,
            'height' : self.height,
            'date_created' : self.date_created,
            'profile_image_path' : self.profile_image_path
        }
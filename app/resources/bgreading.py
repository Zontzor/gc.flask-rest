from app import db

class BGReading(db.Model):
    __tablename__ = 'bg_readings'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(30))
    bg_value = db.Column('bg_value', db.Float)
    bg_timestamp = db.Column('bg_timestamp', db.DateTime)
    
    def serialize(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'bg_value' : self.bg_value,
            'bg_timestamp' : self.bg_timestamp
        }
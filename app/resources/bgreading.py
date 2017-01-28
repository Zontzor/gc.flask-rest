from app import db

class BGReading(db.Model):
    __tablename__ = 'bg_readings'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer)
    bg_value = db.Column('bg_value', db.Float)
    bg_timestamp = db.Column('bg_timestamp', db.DateTime)
    
    def serialize(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'bg_value' : self.bg_value,
            'bg_timestamp' : self.bg_timestamp
        }
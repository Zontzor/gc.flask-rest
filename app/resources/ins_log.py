"""
    Author: Alex Kiernan

    Desc: Insulin dosage model
"""
from app import db

class InsDosage(db.Model):
    __tablename__ = 'insulin_logs'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer)
    ins_type = db.Column('ins_type', db.String(30))
    ins_value = db.Column('ins_value', db.Float)
    ins_timestamp = db.Column('ins_timestamp', db.DateTime)

    def serialize(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'ins_type' : self.ins_type,
            'ins_value' : self.ins_value,
            'ins_timestamp' : self.ins_timestamp,
        }

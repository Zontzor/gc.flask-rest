"""
    Author: Alex Kiernan

    Desc: Food log model
"""
from app import db


class FoodLog(db.Model):
    __tablename__ = 'food_logs'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer)
    food_id = db.Column('food_id', db.Integer)
    fl_quantity = db.Column('fl_quantity', db.Float)
    fl_timestamp = db.Column('fl_timestamp', db.DateTime)

    def serialize(self):
        return {
            'id' : self.id,
            'user_id' : self.user_id,
            'food_id' : self.food_id,
            'fl_quantity' : self.fl_quantity,
            'fl_timestamp' : self.fl_timestamp,
        }

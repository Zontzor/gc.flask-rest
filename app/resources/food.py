"""
    Author: Alex Kiernan

    Desc: Food model
"""
from app import db


class Food(db.Model):
    __tablename__ = 'foods'
    id = db.Column('id', db.Integer, primary_key=True)
    f_name = db.Column('f_name', db.String(30))
    f_carbs = db.Column('f_carbs', db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'f_name': self.f_name,
            'f_carbs': self.f_carbs,
        }
"""
    Author: Alex Kiernan

    Desc: Exercise model
"""
from app import db


class Exercise(db.Model):
    __tablename__ = 'exercises'
    id = db.Column('id', db.Integer, primary_key=True)
    e_name = db.Column('e_name', db.String(30))
    e_energy_phour = db.Column('e_energy_phour', db.Integer)

    def serialize(self):
        return {
            'id': self.id,
            'e_name': self.e_name,
            'e_energy_phour': self.e_energy_phour,
        }

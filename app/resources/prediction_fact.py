from app import db


class PredictionFact(db.Model):
    __tablename__ = 'predicition_facts'
    id = db.Column('id', db.Integer, primary_key=True)
    pf_date = db.Column('pf_date', db.Date)
    pf_time_of_day = db.Column('pf_time_of_day', db.Integer)
    user_id = db.Column('user_id', db.Integer)
    bg_value = db.Column('bg_value', db.Float)
    ins_value = db.Column('ins_value', db.Float)
    food_value = db.Column('food_value', db.Float)
    exercise_value = db.Column('exercise_value', db.Float)

    def serialize(self):
        return {
            'id' : self.id,
            'pf_date' : self.pf_date,
            'pf_time_of_day' : self.pf_time_of_day,
            'user_id' : self.user_id,
            'bg_value' : self.bg_value,
            'ins_value': self.ins_value,
            'food_value': self.food_value,
            'exercise_value': self.exercise_value
        }
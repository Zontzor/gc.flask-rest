from app import db


class Fact(db.Model):
    __tablename__ = 'prediction_facts'
    pf_date = db.Column('pf_date', db.Date, primary_key=True)
    pf_time_of_day = db.Column('pf_time_of_day', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer, primary_key=True)
    bg_value = db.Column('bg_value', db.Float)
    ins_value = db.Column('ins_value', db.Float)
    food_value = db.Column('food_value', db.Integer)
    exercise_value = db.Column('exercise_value', db.Integer)

    def serialize(self):
        return {
            'pf_date' : self.pf_time_of_day,
            'pf_time_of_day' : self.pf_time_of_day,
            'user_id' : self.user_id,
            'bg_value' : self.bg_value,
            'ins_value': self.ins_value,
            'food_value': self.food_value,
            'exercise_value': self.exercise_value
        }

    def fact_serialize(self):
        return {
            'timestamp': self.pf_time_of_day,
            'bg_value': self.bg_value,
            'carbs': self.food_value,
            'exercise': self.exercise_value,
            'insulin_dosage': self.ins_value
        }
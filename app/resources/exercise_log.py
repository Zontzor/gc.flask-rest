from app import db


class ExerciseLog(db.Model):
    __tablename__ = 'exercise_logs'
    id = db.Column('id', db.Integer, primary_key=True)
    user_id = db.Column('user_id', db.Integer)
    exercise_id = db.Column('exercise_id', db.Integer)
    el_duration = db.Column('el_duration', db.Integer)
    el_timestamp = db.Column('el_timestamp', db.DateTime)

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'exercise_id': self.exercise_id,
            'el_duration': self.el_duration,
            'el_timestamp': self.el_timestamp,
        }
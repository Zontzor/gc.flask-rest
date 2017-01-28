from app import app
from flask import jsonify 
from ..resources.user import User
from ..resources.bgreading import BGReading

@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/bgreadings', 
methods=['GET'])
def get_user_bgreadings(user_name):
    user = User.query.filter_by(username=user_name).first()
    data = BGReading.query.filter_by(username=user_name).all()
    data_all = []
    
    for bgreading in data:
        data_all.append(bgreading.serialize()) 
    
    if user is None:
        abort(404)
        
    return jsonify(bgreadings=data_all)
    
@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/bgreadings', 
methods=['POST'])
def add_bg(user_name):
    username = request.get_json()['username']
    bg_value = request.get_json()['bg_value']
    bg_timestamp = request.get_json()['bg_timestamp']
    
    bg_reading = BGReading(username = username, bg_value = bg_value, 
    bg_timestamp = bg_timestamp)
    
    user = User.query.filter_by(username=user_name).first()
    
    if user is None:
        abort(404)
    
    curr_session = db.session #open database session
    try:
        curr_session.add(bg_reading) #add prepared statment to opened session
        curr_session.commit() #commit changes
    except:
        curr_session.rollback()
        curr_session.flush() 
        print("Add bgreading error")
    
    return jsonify(bg_reading.serialize())

"""@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/bgreadings/<string:datestamp>', 
methods=['GET'])
def get_user_bgreadings_day(user_name, datestamp):
    user = User.query.filter_by(username=user_name).first()
    data = BGReading.query.filter_by(username=user_name).all()
    data_all = []
    
    # Parse date from each bg reading and match to users requested date
    for bgreading in data:
        date = dateutil.parser.parse(str(bgreading.bg_timestamp)).date()
        if (datestamp == str(date)):
            data_all.append(bgreading.serialize()) 
    
    if user is None:
        abort(404)
        
    return jsonify(bgreadings=data_all)"""

"""
    Author: Alex Kiernan

    Desc: BG logs routes
"""
from app import app, db, auth
from flask import jsonify, request, abort
from ..resources.user import User
from ..resources.bg_log import BGReading


@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/bgreadings', methods=['GET'])
@auth.login_required
def read_all_bgs(user_name):
    user = User.query.filter_by(username=user_name).first()
    
    if user is None:
        abort(404)
        
    data = BGReading.query.filter_by(user_id=user.id).all()
    data_all = []
    
    for bgreading in data:
        data_all.append(bgreading.serialize()) 
        
    return jsonify(data_all)


@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/bgreadings/<int:bg_id>', methods=['GET'])
@auth.login_required
def read_bgs(user_name, bg_id):
    user = User.query.filter_by(username=user_name).first()
    
    if user is None:
        abort(404)
        
    bg_reading = BGReading.query.filter_by(id=bg_id).first()
    
    if bg_reading is None:
        abort(404)

    return jsonify(bg_reading.serialize())


@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/bgreadings', methods=['POST'])
@auth.login_required
def create_bg(user_name):
    bg_value = request.get_json()['bg_value']
    bg_timestamp = request.get_json()['bg_timestamp']
    
    user = User.query.filter_by(username=user_name).first()
    
    if user is None:
        abort(404)
    
    bg_reading = BGReading(user_id = user.id, bg_value = bg_value, 
    bg_timestamp = bg_timestamp)
    
    curr_session = db.session # Open database session
    try:
        curr_session.add(bg_reading) # Add prepared statement to opened session
        curr_session.commit() # Commit changes
    except:
        curr_session.rollback()
        curr_session.flush() 
        print("Add bgreading error")
    
    return jsonify(bg_reading.serialize())


@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/bgreadings/<int:bg_id>', methods=['PUT'])
@auth.login_required
def update_bg(user_name, bg_id):
    user = User.query.filter_by(username=user_name).first()
    
    if user is None:
        abort(404)
        
    bg_reading = BGReading.query.filter_by(id=bg_id).first()
    
    if bg_reading is None:
        abort(404)
    
    curr_session = db.session 
    try:
        if 'bg_value' in request.json:
            bg_reading.bg_value = request.get_json()['bg_value'] 
        if 'bg_timestamp' in request.json:
            bg_reading.bg_timestamp = request.get_json()['bg_timestamp']
        
        curr_session.commit()
    except:
        curr_session.rollback()
        curr_session.flush()

    return jsonify(bg_reading.serialize())

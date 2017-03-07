from app import app, db, auth
from flask import jsonify, request, abort
from ..resources.user import User
from ..resources.ins_log import InsDosage

@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/insdosages', methods=['GET'])
@auth.login_required
def read_all_ins(user_name):
    user = User.query.filter_by(username=user_name).first()
    
    if user is None:
        abort(404)
        
    data = InsDosage.query.filter_by(user_id=user.id).all()
    data_all = []
    
    for ins_dosage in data:
        data_all.append(ins_dosage.serialize()) 
        
    return jsonify(data_all)

@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/insdosages/<int:ins_id>', methods=['GET'])
@auth.login_required
def read_ins(user_name, ins_id):
    user = User.query.filter_by(username=user_name).first()
    
    if user is None:
        abort(404)
        
    ins_dosage = InsDosage.query.filter_by(id=ins_id).first()
    
    if ins_dosage is None:
        abort(404)

    return jsonify(ins_dosage.serialize())
    
@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/insdosages', methods=['POST'])
@auth.login_required
def create_ins(user_name):
    ins_type = request.get_json()['ins_type']
    ins_value = request.get_json()['ins_value']
    ins_timestamp = request.get_json()['ins_timestamp']
    
    user = User.query.filter_by(username=user_name).first()
    
    if user is None:
        abort(404)
    
    ins_dosage = InsDosage(user_id = user.id, ins_type = ins_type, 
        ins_value = ins_value, ins_timestamp = ins_timestamp)
    
    curr_session = db.session #open database session
    try:
        curr_session.add(ins_dosage) #add prepared statment to opened session
        curr_session.commit() #commit changes
    except:
        curr_session.rollback()
        curr_session.flush() 
        print("Add bgreading error")
    
    return jsonify(ins_dosage.serialize())
    
@app.route('/glucose_coach/api/v1.0/users/<string:user_name>/insdosages/<int:ins_id>', methods=['PUT'])
@auth.login_required
def update_ins(user_name, ins_id):
    user = User.query.filter_by(username=user_name).first()
    
    if user is None:
        abort(404)
        
    ins_dosage = InsDosage.query.filter_by(id=ins_id).first()
    
    if ins_dosage is None:
        abort(404)
    
    curr_session = db.session 
    try:
        if 'ins_type' in request.json:
            ins_dosage.ins_type = request.get_json()['ins_type']
        if 'ins_value' in request.json:
            ins_dosage.ins_value = request.get_json()['ins_value'] 
        if 'bg_timestamp' in request.json:
            ins_dosage.ins_timestamp = request.get_json()['bg_timestamp']
        
        curr_session.commit()
    except:
        curr_session.rollback()
        curr_session.flush()

    return jsonify(ins_dosage.serialize())
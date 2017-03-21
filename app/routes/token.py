"""
    Author: Alex Kiernan

    Desc: Get a token
"""
from app import app, auth
from flask import jsonify, g


@app.route('/glucose_coach/api/v1.0/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })

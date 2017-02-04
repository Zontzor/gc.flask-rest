from app import app, db, auth
from flask import Flask, jsonify, request, abort, make_response, g
from ..resources.user import User

@app.route('/glucose_coach/api/v1.0/token')
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token()
    return jsonify({ 'token': token.decode('ascii') })
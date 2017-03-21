"""
    Author: Alex Kiernan

    Desc: Authenticates user using either a token or username/password
"""
from app import auth
from flask import g
from ..resources.user import User


@auth.verify_password
def verify_password(username_or_token, password):
    # First try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # Try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

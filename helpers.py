from flask import request, abort
from functools import wraps
from flask_login import current_user

def is_admin(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.role == 'admin':
            return func(*args, **kwargs)
        return abort(401)
    return decorated_function

def same_user(func):
    @wraps(func)
    def decorated_function(*args, email, **kwargs):
        if current_user.email != email:
            return abort(403)
        return func(*args, email=email, **kwargs)
    return decorated_function
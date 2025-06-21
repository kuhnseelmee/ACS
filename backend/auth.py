
import bcrypt
from flask import request, jsonify
from flask_jwt_extended import create_access_token, get_jwt
from db import get_db

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())

def login():
    data = request.json
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM users WHERE username=%s", (data['username'],))
    user = cursor.fetchone()
    if user and check_password(data['password'], user['password_hash']):
        cursor.execute("SELECT name FROM roles WHERE id=%s", (user['role_id'],))
        role = cursor.fetchone()['name']
        access_token = create_access_token(identity=user['id'], additional_claims={
            'role': role,
            'tenant_id': user['tenant_id']
        })
        return jsonify(access_token=access_token)
    return jsonify({'msg': 'Bad credentials'}), 401

from functools import wraps
from flask import abort
from flask_jwt_extended import get_jwt

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get('role') not in roles:
                abort(403, description="Forbidden: Insufficient role")
            return fn(*args, **kwargs)
        return decorator
    return wrapper

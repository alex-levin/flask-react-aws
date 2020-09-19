# services/users/project/api/auth.py


import jwt
from flask import Blueprint, request, make_response, jsonify

from project import bcrypt
from project.api.users.crud import add_user, get_user_by_email, get_user_by_id
from project.api.users.models import User

auth_blueprint = Blueprint('auth', __name__)


# App.jsx: const url = `${process.env.REACT_APP_USERS_SERVICE_URL}/auth/register`;
@auth_blueprint.route('/api/auth/register/', methods=['POST'])
def register():
    print(request)
    post_data = request.get_json()
    username = post_data['username']
    email = post_data['email']
    password = post_data['password']
    response_object = {}
    user = get_user_by_email(email)
    if user:
        response_object["message"] = "Sorry. That email already exists."
        return response_object, 400
    add_user(username, email, password)
    response_object["message"] = f"{email} was added!"
    return response_object, 201


@auth_blueprint.route('/api/auth/login/', methods=['POST'])
def login():
    post_data = request.get_json()
    email = post_data['email']
    password = post_data['password']
    response_object = {}
    user = get_user_by_email(email)
    if not user or not bcrypt.check_password_hash(user.password, password):
        response_object["message"] = "User does not exist"
        return response_object, 404

    access_token = user.encode_token(user.id, "access")
    refresh_token = user.encode_token(user.id, "refresh")

    response_object = {
        'status': 'success',
        'message': 'Successfully logged in.',        
        "access_token": access_token.decode(),
        "refresh_token": refresh_token.decode(),
    }
    # return make_response(jsonify(responseObject)), 200 - no longer needed
    return response_object, 200

@auth_blueprint.route('/api/auth/refresh/', methods=['POST'])
def refresh():
    post_data = request.get_json()
    refresh_token = post_data['refresh_token']
    response_object = {}
    try:
        resp = User.decode_token(refresh_token)
        user = get_user_by_id(resp)
        if not user:
            response_object["message"] = "Invalid token"
            return response_object, 401   
        access_token = user.encode_token(user.id, "access")
        refresh_token = user.encode_token(user.id, "refresh")

        response_object = {
            "access_token": access_token.decode(),
            "refresh_token": refresh_token.decode(),
        }
        return response_object, 200
    except jwt.ExpiredSignatureError:
        auth_namespace.abort(401, "Signature expired. Please log in again.")
        return "Signature expired. Please log in again."
    except jwt.InvalidTokenError:
        auth_namespace.abort(401, "Invalid token. Please log in again.")    


@auth_blueprint.route('/api/auth/status/', methods=['GET'])
def get_status():
    auth_header = request.headers.get("Authorization")
    response_object = {}
    if auth_header:
        try:
            access_token = auth_header.split(" ")[1]
            resp = User.decode_token(access_token)
            user = get_user_by_id(resp)
            if not user:
                response_object['message'] = "Invalid token"
                return response_object, 401   
            response_object['username'] = user.username
            response_object['email'] = user.email
            return response_object, 200 
        except jwt.ExpiredSignatureError:
            response_object["message"] = "Signature expired. Please log in again."
            return response_object, 401            
        except jwt.InvalidTokenError:
            response_object["message"] = "Invalid token. Please log in again."
            return response_object, 401            
    else:
        auth_namespace.abort(403, "Token required")
        response_object["message"] = "Token required."
        return response_object, 403            

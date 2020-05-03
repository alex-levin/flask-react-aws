# services/users/project/api/users/views.py


# from flask import request
from flask import Blueprint, jsonify, request
from flask_restx import Resource, fields, Namespace

from project.api.users.crud import (
    get_all_users,
    get_user_by_email,
    add_user,
    get_user_by_id,
    update_user,
    delete_user,
)


users_namespace = Namespace("users")


users_blueprint = Blueprint('users', __name__)


user = users_namespace.model(
    "User",
    {
        "id": fields.Integer(readOnly=True),
        "username": fields.String(required=True),
        "email": fields.String(required=True),
        "created_date": fields.DateTime,
    },
)


@users_blueprint.route('/api/users/', methods=['GET'])
def get_users():
    """Get all users"""
    data = []
    users = get_all_users()
    for row in users:
        data.append(row.to_json())
    response = jsonify(data)
    return response


@users_blueprint.route('/api/users/', methods=['POST'])
def post_user():
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        password = post_data.get("password")
        response_object = {}

        user = get_user_by_email(email)
        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400
        add_user(username, email, password)
        response_object["message"] = f"{email} was added!"
        return response_object, 201


@users_blueprint.route('/api/users/<email>', methods=['GET'])    
def get_email(email):
    response_object = {}
    user = get_user_by_email(email)
    if not user:
        response_object["message"] = f"{email} was not found!"
        return response_object, 404
    data = user.to_json()
    response = jsonify(data)
    return response


@users_blueprint.route('/api/users/<int:id>', methods=['GET'])    
def get_id(id):
    user = get_user_by_id(id)
    if not user:
        response_object["message"] = f"{id} was not found!"
        return response_object, 404
    data = user.to_json()
    response = jsonify(data)
    return response


@users_blueprint.route('/api/users/<int:id>', methods=['PUT'])    
def put_id(id):
    put_data = request.get_json()
    username = put_data.get("username")
    email = put_data.get("email")

    response_object = {}
    user = get_user_by_id(id)
    if not user:
        response_object["message"] = f"{user.id} was not found!"
        return response_object, 404
    
    update_user(user, username, email)
    response_object["message"] = f"{user.id} was updated!"
    return response_object, 200


@users_blueprint.route('/api/users/<int:id>', methods=['DELETE'])
def delete_id(id):
    response_object = {}
    user = get_user_by_id(id)
    if not user:
        response_object["message"] = f"{user.id} was not found!"
        return response_object, 404    
    delete_user(user)
    response_object["message"] = f"{user.id} was removed!"
    return response_object, 200    


user_post = users_namespace.inherit(
    "User post", user, {"password": fields.String(required=True)}
)


class UsersList(Resource):
    @users_namespace.marshal_with(user, as_list=True)
    def get(self):
        """Returns all users."""
        return get_all_users(), 200

    @users_namespace.expect(user_post, validate=True)
    @users_namespace.response(201, "<user_email> was added!")
    @users_namespace.response(400, "Sorry. That email already exists.")
    def post(self):
        """Creates a new user."""
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        password = post_data.get("password")
        response_object = {}

        user = get_user_by_email(email)
        if user:
            response_object["message"] = "Sorry. That email already exists."
            return response_object, 400
        add_user(username, email, password)
        response_object["message"] = f"{email} was added!"
        return response_object, 201


class Users(Resource):
    @users_namespace.marshal_with(user)
    @users_namespace.response(200, "Success")
    @users_namespace.response(404, "User <user_id> does not exist")
    def get(self, user_id):
        """Returns a single user."""
        user = get_user_by_id(user_id)
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        return user, 200

    @users_namespace.expect(user, validate=True)
    @users_namespace.response(200, "<user_is> was updated!")
    @users_namespace.response(404, "User <user_id> does not exist")
    def put(self, user_id):
        """Updates a user."""
        post_data = request.get_json()
        username = post_data.get("username")
        email = post_data.get("email")
        response_object = {}

        user = get_user_by_id(user_id)
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        update_user(user, username, email)
        response_object["message"] = f"{user.id} was updated!"
        return response_object, 200

    @users_namespace.response(200, "<user_is> was removed!")
    @users_namespace.response(404, "User <user_id> does not exist")
    def delete(self, user_id):
        """Updates a user."""
        response_object = {}
        user = get_user_by_id(user_id)
        if not user:
            users_namespace.abort(404, f"User {user_id} does not exist")
        delete_user(user)
        response_object["message"] = f"{user.email} was removed!"
        return response_object, 200


users_namespace.add_resource(UsersList, "")
users_namespace.add_resource(Users, "/<int:user_id>")

# services/users/project/api/users/views.py


from flask import Blueprint, jsonify, request


from project.api.users.crud import (
    get_all_users,
    get_user_by_email,
    add_user,
    get_user_by_id,
    update_user,
    delete_user,
)


users_blueprint = Blueprint('users', __name__)


# Using error handler decorators from Flask

@users_blueprint.errorhandler(404)
def not_found(e):
    response = jsonify({'status': 404, 'error': 'not found',
                        'message': 'invalid resource URI'})
    response.status_code = 404
    return response


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
    print(request)
    post_data = request.get_json()
    print(post_data)
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


@users_blueprint.route('/api/users/<email>', methods=['GET'])    
def get_email(email):
    user = get_user_by_email(email)
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




from jsonschema.exceptions import ValidationError

from data import users, UserNotFoundException, UserAlreadyExistsException
from flask import Flask, request

app = Flask(__name__)

API_BASE = '/api/users'


@app.get(API_BASE)
def get_users():
    users_list = users.users_list()
    if users_list:
        return users_list
    return [], 204


@app.get(API_BASE + '/<int:user_id>')
def get_user(user_id):
    try:
        return users.find_user(user_id)
    except UserNotFoundException as e:
        return {'error_message': str(e)}, 404


@app.post(API_BASE)
def create_user():
    user = request.json
    try:
        users.add(user)
        return user, 201
    except ValidationError as e:
        return {'error_message': str(e)}, 400
    except UserAlreadyExistsException as e:
        return {'error_message': str(e)}, 400


@app.delete(API_BASE + '/<int:user_id>')
def delete_user(user_id):
    try:
        return users.delete(user_id)
    except UserNotFoundException as e:
        return {'error_message': str(e)}, 404


if __name__ == '__main__':
    app.run()

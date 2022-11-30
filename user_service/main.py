from jsonschema.exceptions import ValidationError
from requests_oauthlib import OAuth2Session

from data import users, UserNotFoundException, UserAlreadyExistsException
from flask import Flask, request, redirect, jsonify

# https://github.com/settings/applications/new
client_id = "<client_id>"
client_secret = "<client_secret>"

authorization_base_url = 'https://github.com/login/oauth/authorize'
token_url = 'https://github.com/login/oauth/access_token'

app = Flask(__name__)

API_BASE = '/api/users'


@app.route("/")
def home_page():
    github = OAuth2Session(client_id)
    authorization_url, state = github.authorization_url(authorization_base_url)

    print(authorization_url)
    print(state)
    return redirect(authorization_url)


@app.get('/callback')
def callback():
    github = OAuth2Session(client_id)
    token = github.fetch_token(token_url, client_secret=client_secret,
                               authorization_response=request.url)

    # github.token = token
    github = OAuth2Session(client_id, token=token)
    user_info = github.get('https://api.github.com/user').json()
    email = user_info['email']

    return jsonify(email)


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
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.run()

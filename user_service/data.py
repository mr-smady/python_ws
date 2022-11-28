import json
from jsonschema import validate

_USER_SCHEMA = {
    "type": "object",
    "properties": {
        "id": {"type": "number"},
        "email": {"type": "string"},
        "first_name": {"type": "string"},
        "last_name": {"type": "string"},
        "avatar": {"type": "string"},
    },
    "required": ["id", "email", "first_name", "last_name"],
}


class UserNotFoundException(Exception):
    """UserNotFoundException"""


class UserAlreadyExistsException(Exception):
    """UserAlreadyExistsException"""


class _Users:

    def __init__(self):
        with open('data/users.json') as users_file:
            self.__users = json.load(users_file)

    def users_list(self):
        return self.__users

    def find_user(self, user_id):
        user_index = self.__find_user_index(user_id)
        if user_index is None:
            raise UserNotFoundException('user(%s) not found' % user_id)
        return self.__users[user_index]

    def add(self, new_users):
        if not isinstance(new_users, (list, set, tuple)):
            new_users = [new_users]
        for user in new_users:
            validate(instance=user, schema=_USER_SCHEMA)
            if self.__find_user_index(user['id']) is not None:
                raise UserAlreadyExistsException('user(%s) exists' % user['id'])
        self.__users.extend(new_users)
        self.__save()

    def update(self, user):
        validate(instance=user, schema=_USER_SCHEMA)
        user_index = self.__find_user_index(user['id'])
        if user_index is None:
            raise UserNotFoundException('user(%s) not found' % user['id'])
        self.__users[user_index] = user
        self.__save()

    def delete(self, user_id):
        user = self.find_user(user_id)
        self.__users.remove(user)
        return user

    def __find_user_index(self, user_id):
        return next((i for i, user in enumerate(self.__users) if user['id'] == user_id), None)

    def __save(self):
        with open('data/users.json', 'w') as users_file:
            users_file.write(json.dumps(self.__users))


users = _Users()

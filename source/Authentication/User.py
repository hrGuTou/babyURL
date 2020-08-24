from flask_login import UserMixin
from werkzeug.security import check_password_hash
import json
from ..Util.AWSManager import AWSManger

def load():
    try:
        with open('USERS.json', 'r') as f:
            data = json.load(f)
    except Exception as e:
        pass
    else:
        f.close()
        return data


class User(UserMixin):
    def __init__(self, user):
        self.aws = AWSManger()
        self.username = user.get('username')
        self.password = user.get('password')
        self.id = user.get('id')

    def verify(self, password):
        return check_password_hash(self.password, password)

    def getId(self):
        return self.id

    @staticmethod
    def get(user_id):
        aws = AWSManger()
        val = aws.getByID(user_id)
        if val:
            return User(val)

        return None




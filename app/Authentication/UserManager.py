
from werkzeug.security import generate_password_hash
from ..Util.AWSManager import AWSManger
import uuid


class UserManager:
    def __init__(self):
        self.aws = AWSManger()

    def createUser(self, username, password):
        user = {
            "username": username,
            "password": generate_password_hash(password),
            "id": str(uuid.uuid4()),
            "URLHistory": []
        }
        self.aws.saveUser(user)

    def getUser(self, username):
        return self.aws.getUser(username)

    def saveUserURL(self,username, shortURL):
        # save gen short url under current user
        self.aws.saveUserURL(username, shortURL)

import json

from werkzeug.security import generate_password_hash
import uuid


class UserManager:
    def __init__(self):
        self.USERS = {}
        self.load()

    def load(self):
        try:
            with open('USERS.json', 'r') as f:
                self.USERS = json.load(f)
        except Exception as e:
            print(e)
        else:
            f.close()

    def save(self):
        try:
            with open('USERS.json', 'w') as f:
                f.write(json.dumps(self.USERS, indent=4))
        except Exception as e:
            print(e)
        else:
            f.close()

    def getAllUsers(self):
        return self.USERS

    def createUser(self, username, password):
        user = {
            "username": username,
            "password": generate_password_hash(password),
            "id": str(uuid.uuid4()),
            "url": []
        }

        self.USERS[username]=user
        self.save()

    def getUser(self, username):
        if self.USERS:
            if username in self.USERS:
                return self.USERS[username]

    def saveURL(self,username, shortURL):
        # save gen short url under current user
        self.USERS[username]["url"].append(shortURL)
        self.save()

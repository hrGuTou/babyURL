from flask import Flask, request
from flask_login import LoginManager, login_required, login_user, logout_user
from Authentication.UserManager import UserManager
from Authentication.User import User


class API:
    def __init__(self):
        self.app = Flask(__name__)
        self.init()

    def init(self):
        userManager = UserManager()
        self.app.secret_key = "zbc"

        login_manager = LoginManager()
        login_manager.init_app(self.app)
        login_manager.login_view = 'login'

        @login_manager.user_loader
        def load_user(user_id):
            return User.get(user_id)

        @self.app.route('/')
        @login_required
        def hello_world():
            return "hi"


        @self.app.route('/api/short')
        @login_required
        def shorten():
            pass
        # TODO: implementation for shorten url


        @self.app.route('/api/login', methods=["POST"])
        def login():
            res = request.json
            username = res['username']
            password = res['password']
            remember = res['remember']
            user_info = userManager.getUser(username)

            user = User(user_info)
            if user.verify(password):
                login_user(user, remember=remember)
                return "LOGIN!"
            else:
                return "BAD LOGIN"

        @self.app.route('/api/logout')
        @login_required
        def logout():
            logout_user()
            return "OK"

        @self.app.route('/api/create', methods=["POST"])
        def create():
            res = request.json
            username = res['username']
            password = res['password']
            userManager.createUser(username, password)

            return "OK"

    def run(self):
        self.app.run()


if __name__ == "__main__":
    api = API()
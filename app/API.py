import flask_login
from flask import Flask, request, render_template
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.utils import redirect

from app.Authentication.UserManager import UserManager
from app.Authentication.User import User


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

        @login_manager.unauthorized_handler
        def unauthorized_callback():
            return redirect('/login')

        @self.app.route('/')
        @login_required
        def hello_world():
            usr = flask_login.current_user.username
            return render_template('index.html', username=usr)

        @self.app.route('/login', methods=['GET','POST'])
        def login():
            msg = None
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                remember = True if request.form.get('remember') else False

                user_info = userManager.getUser(username)
                if user_info:
                    user = User(user_info)
                    if user.verify(password):
                        login_user(user, remember=remember)
                        return render_template('index.html', username=username)

                msg = "Invalid username/password"
            return render_template('login.html', message=msg)

        @self.app.route('/logout')
        @login_required
        def logout():
            logout_user()
            return redirect('/')

        @self.app.route('/register', methods=["GET", "POST"])
        def create():
            return render_template('register.html')





        @self.app.route('/api/short')
        @login_required
        def shorten():
            pass
        # TODO: implementation for shorten url







    def run(self):
        self.app.run()


if __name__ == "__main__":
    api = API()
import json
from datetime import timedelta

import flask_login
from flask import Flask, request, render_template, session
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.utils import redirect

from source.Authentication.UserManager import UserManager
from source.Authentication.User import User
from source.Util.Convert import *
from source.Util.SnowFlake_Counter import *
from source.Util.AWSManager import AWSManger


class API:
    def __init__(self):
        self.app = Flask(__name__)
        self.aws = AWSManger()
        self.counter = generator(1,1)
        self.init()


    def init(self):
        userManager = UserManager()
        self.app.secret_key = "zbc"

        login_manager = LoginManager()
        login_manager.init_app(self.app)
        login_manager.login_view = 'login'
        login_manager.refresh_view = 'relogin'
        login_manager.needs_refresh_message = (u"Session timedout, please re-login")
        login_manager.needs_refresh_message_category = "info"

        @self.app.before_request
        def before_request():
            session.permanent = True
            self.app.permanent_session_lifetime = timedelta(seconds=10)

        @login_manager.user_loader
        def load_user(user_id):
            return User.get(user_id)

        @login_manager.unauthorized_handler
        def unauthorized_callback():
            return redirect('/login')

        @self.app.route('/', methods=['GET', 'POST'])
        @login_required
        def main():
            usr = flask_login.current_user.username
            shortURL = None

            if request.method == 'POST':
                longURL = request.form['longurl']
                shortURL = self.shorten(longURL)
                userManager.saveUserURL(usr, shortURL)
                return render_template('index.html', username=usr, shortURL=shortURL)

            return render_template('index.html', username=usr, shortURL=shortURL)

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
                        return redirect('/')

                msg = "Invalid username/password"
            return render_template('login.html', message=msg)

        @self.app.route('/logout')
        @login_required
        def logout():
            logout_user()
            return redirect('/')

        @self.app.route('/register', methods=["GET", "POST"])
        def create():
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                userManager.createUser(username, password)
                return redirect('/login')
            return render_template('register.html')

        @self.app.errorhandler(404)
        @self.app.route('/<shortURL>')
        def decodeURL(shortURL):
            id = str(toBase10(shortURL))
            longURL = self.aws.getURL(id)
            if longURL:
                return redirect(longURL, code=302)

            return render_template('404.html'), 404

    def shorten(self, longURL):
        id = self.counter.__next__()
        self.aws.saveURL(id, longURL)
        shortURL = toBase62(id)
        return shortURL

    def run(self):
        self.app.run()


if __name__ == "__main__":
    api = API()
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
from source.Cache.cache import Cache
from source.Util.REDISManager import REDISManager


class API:
    def __init__(self):
        self.app = Flask(__name__)
        self.aws = AWSManger()
        self.redis = REDISManager()
        self.counter = generator(1,1)
        self.cache = Cache()
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
                id = self.counter.__next__()

                longURL = request.form['longurl']
                shortURL = toBase62(id)

                if self.cache.cache_get(longURL) == -1:
                    # if current input is not in cache, then save in cache and insert into db
                    self.cache.cache_put(longURL, shortURL)
                    userManager.saveUserURL(usr, shortURL)
                    self.aws.saveURL(id, longURL)
                else:
                    # if current input is in cache, read from cache
                    shortURL = self.cache.cache_get(longURL)
                    print('read from cache')
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
            msg = None
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                pswRepeat = request.form['psw-repeat']
                if not password == pswRepeat:
                    msg = 'Password not match, try again'
                    return render_template('register.html', message=msg)

                userManager.createUser(username, password)
                return redirect('/login')
            return render_template('register.html', message=msg)

        @self.app.errorhandler(404)
        @self.app.route('/<shortURL>')
        def decodeURL(shortURL):
            print(shortURL)
            id = str(toBase10(shortURL))
            print(id)
            # try to get from redis first
            # if found in redis, return from redis
            longURL = self.redis.get_from_redis(id)
            #print(longURL)

            if longURL is None:
                # not in redis, get from DB, then update redis
                longURL = self.aws.getURL(id)

                if longURL:
                    self.redis.add_to_redis(id, longURL)
                    return redirect(longURL, code=302)
                else:
                    return render_template('404.html'), 404

            return redirect(longURL, code=302)


    def run(self):
        self.app.run(host='0.0.0.0', port=5000)


if __name__ == "__main__":
    api = API()
    api.run()
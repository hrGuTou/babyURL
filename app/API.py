from datetime import timedelta

import flask_login
from flask import Flask, request, render_template, session, send_from_directory, Blueprint
from flask_login import LoginManager, login_required, login_user, logout_user
from werkzeug.utils import redirect

from app.Authentication.UserManager import UserManager
from app.Authentication.User import User
from app.Util.Convert import *
from app.Util.SnowFlake_Counter import *
from app.Util.AWSManager import AWSManger
from app.Cache.cache import Cache
from app.Util.REDISManager import REDISManager


import pyqrcode, requests
import os


api = Blueprint('api', __name__)

aws = AWSManger()
redis = REDISManager()
counter = generator(1,1)
cache = Cache()
userManager = UserManager()


@api.before_request
def before_request():
            session.permanent = True
            api.permanent_session_lifetime = timedelta(minutes=5)


@api.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(api.root_path, 'static'),
                                       'favicon.ico', mimetype='image/vnd.microsoft.icon')


@api.route('/', methods=['GET', 'POST'])
@login_required
def main():
            usr = flask_login.current_user.username
            shortURL = None
            strimg = None
            ErrorMsg = None

            if request.method == 'POST':
                id = counter.__next__()

                longURL = request.form['longurl']
                try:
                    r = requests.get(longURL)
                except:
                    ErrorMsg = "Invalid URL, please try again"
                    return render_template('index.html', username=usr, shortURL=shortURL, qr=strimg, error=ErrorMsg)

                shortURL = toBase62(id)

                if cache.cache_get(longURL) == -1:
                    # if current input is not in cache, then save in cache and insert into DB
                    cache.cache_put(longURL, shortURL)
                    userManager.saveUserURL(usr, shortURL)
                    aws.saveURL(id, longURL)
                else:
                    # if current input is in cache, read from cache
                    shortURL = cache.cache_get(longURL)
                    print('read from cache')

            if shortURL:
                # create qrcode svg
                url = os.getenv('DOMAIN') + shortURL
                qrcode = pyqrcode.create(url)
                strimg = qrcode.png_as_base64_str(scale=6)

            return render_template('index.html', username=usr, shortURL=shortURL, qr=strimg, error=ErrorMsg)


@api.route('/login', methods=['GET','POST'])
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


@api.route('/logout')
@login_required
def logout():
            logout_user()
            return redirect('/')


@api.route('/register', methods=["GET", "POST"])
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


@api.errorhandler(404)
@api.route('/<string:shortURL>')
def decodeURL(shortURL):
            if not shortURL.isalnum():
                return render_template('404.html'), 404

            print(shortURL)
            id = str(toBase10(shortURL))
            # try to get from redis first
            # if found in redis, return from redis
            longURL = redis.get_from_redis(id)

            if longURL is None:
                # not in redis, get from DB, then update redis
                longURL = aws.getURL(id)

                if longURL:
                    redis.add_to_redis(id, longURL)
                    return redirect(longURL, code=302)
                else:
                    return render_template('404.html'), 404

            return redirect(longURL, code=302)


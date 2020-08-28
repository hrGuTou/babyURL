from dotenv import load_dotenv
load_dotenv()
from flask_login import LoginManager
from werkzeug.utils import redirect
from app.API import api
from flask import Flask
from app.Authentication.User import User

app = Flask(__name__)
app.register_blueprint(api)
app.secret_key = 'giao!'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.refresh_view = 'relogin'
login_manager.needs_refresh_message = u"Session timedout, please re-login"
login_manager.needs_refresh_message_category = "info"

@login_manager.user_loader
def load_user(user_id):
            return User.get(user_id)

@login_manager.unauthorized_handler
def unauthorized_callback():
            return redirect('/login')


if __name__ == "__main__":
    app.run()
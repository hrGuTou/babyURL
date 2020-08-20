from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/user/<longURL>')
def profile(longURL):
    return "babyurl.com/"

app.run()
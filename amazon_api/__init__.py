from flask import Flask
import flask
from flask_login import LoginManager
import json
import urllib3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

with open('/etc/config.json') as config_file:
  config = json.load(config_file)

app.config['SECRET_KEY'] = config.get('SECRET_KEY')


login_manager = LoginManager()
login_manager.init_app(app)

from amazon_api import api_amz
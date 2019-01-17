import sys
import os
sys.path.append(os.getcwd())

from flask import Flask
from werkzeug import wsgi
# from dashapp.dashapp import app as dashapp


application = Flask(__name__)

from flaskapp import routes

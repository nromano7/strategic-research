from flask import Flask
from werkzeug import wsgi
# from dashapp.dashapp import app as dashapp

app = Flask(__name__)

# app.wsgi_app = wsgi.DispatcherMiddleware(app.wsgi_app, {'/dash',dashapp.server})

from flaskapp import routes


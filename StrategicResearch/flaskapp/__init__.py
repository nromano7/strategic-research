from flask import Flask
from elasticsearch import Elasticsearch

app = Flask(__name__)
client = Elasticsearch()

from flaskapp import routes


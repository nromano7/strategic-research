import sys
import os
sys.path.append(os.getcwd())

from elasticsearch import Elasticsearch

client = Elasticsearch()

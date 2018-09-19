import sys
import os
sys.path.append(os.getcwd())

from elasticsearch import Elasticsearch
import json

# initialize elastic search client
# AWS_EP = r"https://search-strategic-research-eqhxwqugitmyfpzyiobs2dadue.us-east-1.es.amazonaws.com"
client = Elasticsearch()

# states geo JSON
def getStatesGeo():
	with open('./statesGeo.json','r') as f:
		geo = json.load(f)
	return geo
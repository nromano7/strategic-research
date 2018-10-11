import sys
import os
sys.path.append(os.getcwd())

from elasticsearch import Elasticsearch
import json

# initialize elastic search client
AWS_EP = "https://search-strategic-research-67yfnme5nbl3c45vigirwnko4q.us-east-2.es.amazonaws.com"
client = Elasticsearch()

# states geo JSON
def getStatesGeo():
	with open('./statesGeo.json','r') as f:
		geo = json.load(f)
	return geo
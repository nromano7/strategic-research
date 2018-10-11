import sys
import os
sys.path.append(os.getcwd())

from elasticsearch import Elasticsearch
AWS_EP = "https://search-strategic-research-67yfnme5nbl3c45vigirwnko4q.us-east-2.es.amazonaws.com"
client = Elasticsearch(AWS_EP)
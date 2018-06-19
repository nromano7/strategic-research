from datetime import datetime
from elasticsearch import Elasticsearch
import json
from os import listdir, path

PUB_FILES_PATH = r"C:\Users\Nick\Documents\Projects\LTBP\Strategic Research\bulk_20180608\transformed\publications"
AWS_EP = r"https://elastic:wigWgahDPGf7Kh2JetHvcf3x@6c09a7dc67e4408c93e1416ac9bbc629.us-east-1.aws.found.io:9243"

all_pubs_json = listdir(PUB_FILES_PATH)
# es = Elasticsearch(AWS_EP,verify_certs=True)
es = Elasticsearch()

# index publications
index = 'publications'
for file in all_pubs_json:
  id = file.split('_')[1].split('.')[0]
  file_path = path.join(PUB_FILES_PATH,file)
  with open(file_path, 'r') as f:
    doc = json.load(f)
    res = es.index(index=index, doc_type='_doc', id=id, body=doc)
    print(f'[{index} doc:{id}] {res["result"]}')


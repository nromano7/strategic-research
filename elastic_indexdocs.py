from datetime import datetime
from elasticsearch import Elasticsearch
import json
from os import listdir, path
import sys

AWS_EP = r"https://elastic:wigWgahDPGf7Kh2JetHvcf3x@6c09a7dc67e4408c93e1416ac9bbc629.us-east-1.aws.found.io:9243"
PROJECT_FILES_PATH = r"C:\Users\Nick\Documents\Projects\LTBP\Strategic Research\bulk_20180608\transformed\projects"
PUB_FILES_PATH = r"C:\Users\Nick\Documents\Projects\LTBP\Strategic Research\bulk_20180608\transformed\publications"

DOC_TYPE = 'doc'

def indexDocuments(index,root_path):
  esClient = Elasticsearch()
  all_files = listdir(root_path)
  for file in all_files:
    id = file.split('_')[1].split('.')[0]
    file_path = path.join(root_path,file)
    with open(file_path, 'r') as f:
      doc = json.load(f)
      res = esClient.index(index=index, doc_type=DOC_TYPE, id=id, body=doc)
      print(f'[{index} doc:{id}] {res["result"]}')

if 'projects' in sys.argv:
  index = "projects"
  indexDocuments(index, PROJECT_FILES_PATH)
elif 'publications' in sys.argv:
  index = 'publications'
  indexDocuments(index, PUB_FILES_PATH)
else:
  raise(Exception('no arguments provided.'))
from datetime import datetime
from elasticsearch import Elasticsearch
import json
from os import listdir, path
import sys

AWS_EP = r"https://search-strategic-research-eqhxwqugitmyfpzyiobs2dadue.us-east-1.es.amazonaws.com/"
PROJECT_FILES_PATH = r"C:\Users\nickp\OneDrive\Documents\work\projects\ltbp\strategic-research\data-files\20180803\json\projects"
PUB_FILES_PATH = r"C:\Users\nickp\OneDrive\Documents\work\projects\ltbp\strategic-research\data-files\20180803\json\publications"

DOC_TYPE = 'doc'

def indexDocuments(index, root_path):
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
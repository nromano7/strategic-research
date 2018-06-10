from datetime import datetime
from elasticsearch import Elasticsearch
import json
from os import listdir, path

PUB_FILES_PATH = r"C:\Users\Nick\Documents\Projects\LTBP\Strategic Research\bulk_20180608\transformed\publications"
PROJECT_FILES_PATH = r"C:\Users\Nick\Documents\Projects\LTBP\Strategic Research\bulk_20180608\transformed\projects"

all_pub_json = listdir(PUB_FILES_PATH)
all_project_json = listdir(PROJECT_FILES_PATH)
es = Elasticsearch()

# index publications
index = 'trid-publications'
for file in all_pub_json:
  id = file.split('_')[1]
  file_path = path.join(PUB_FILES_PATH,file)
  with open(file_path, 'r') as f:
    doc = json.load(f)
    res = es.index(index="trid", doc_type='project', id=id, body=doc)
    print(f'[{index} doc:{id}] {res["result"]}')

# index projects
index = 'trid-projects'
for file in all_pub_json:
  id = file.split('_')[1]
  file_path = path.join(PUB_FILES_PATH,file)
  with open(file_path, 'r') as f:
    doc = json.load(f)
    res = es.index(index="trid", doc_type='project', id=id, body=doc)
    print(f'[{index} doc:{id}] {res["result"]}')





# res = es.get(index="test-index", doc_type='record', id=1)
# print(res['_source'])

# es.indices.refresh(index="test-index")

# res = es.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
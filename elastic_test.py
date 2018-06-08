from datetime import datetime
from elasticsearch import Elasticsearch
import json
from os import listdir

all_json = listdir('./files/transformed/json/')
es = Elasticsearch()

id = 0
for file in all_json:
  id+=1
  with open(f'./files/transformed/json/{file}', 'r') as f:
    doc = json.load(f)
    res = es.index(index="trid", doc_type='doc', id=id, body=doc)
    print(f'[doc:{id}] {res["result"]}')





# res = es.get(index="test-index", doc_type='record', id=1)
# print(res['_source'])

# es.indices.refresh(index="test-index")

# res = es.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
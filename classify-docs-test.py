from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from models import Project

# initialize elastic search client and search object
AWS_EP = r"https://search-strategic-research-eqhxwqugitmyfpzyiobs2dadue.us-east-1.es.amazonaws.com"
client = Elasticsearch(AWS_EP)
s = Search(using=client,index=index)

# specify index, doc type and query fields
index = 'projects'
doc_type = 'doc'
fields = ["title","abstract"]

q = Q(
  {
    "multi_match":{
      "query": tag,
      "type":"best_fields",
      "fields": fields
    }
  }
)
 
response = s.query(q)
count = response.count()
print(f'[{count} Hit(s) for Tag = "{tag}"]')

for r in response.scan():
  id = r.meta.id
  doc = Project.get(using=client,index=index,id=id)
  tags = list(doc.tags)
  tags.append(tag)
  tag_set = set(tags)
  doc.update(using=client,index=index,tags=list(tag_set))
  print(f'\tDoc ({id}): updated')

  




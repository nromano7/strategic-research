from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q
import query
from models import Project, Publication
import sys

if 'projects' in sys.argv:
  index = "projects"
elif 'publications' in sys.argv:
  index = 'publications'
else:
  raise(Exception('no arguments provided.'))

AWS_EP = "https://search-strategic-research-67yfnme5nbl3c45vigirwnko4q.us-east-2.es.amazonaws.com"
client = Elasticsearch(AWS_EP)

categories = [
  'construction_quality','design_and_details','material_specifications',
  'live_load', 'environment', 'maintenance_and_preservation',
  'structural_integrity', 'structural_condition', 'functionality', 'cost'
]
  
elements = ['deck','overlay','joints','bearings']

def remove_tags(index):
  q = Q({"match_all": {}})
  r = query.run_query(index, q)
  hits = query.process_response(r)

  for id in hits:
    if index == 'projects':
      doc = Project.get(using=client, index=index, id=id)
    elif index == 'publications':
      doc = Publication.get(using=client, index=index, id=id)

    doc.update(using=client,index=index,tags=list(),element_tags=list())
    print(f'{index} - doc ({id}): updated')

remove_tags(index)

for category in categories:
  q = query.get_topic_query(category, None, index)
  r = query.run_query(index, q)
  hits = query.process_response(r)
  for id in hits:
    if index == 'projects':
      doc = Project.get(using=client, index=index, id=id)
    elif index == 'publications':
      doc = Publication.get(using=client, index=index, id=id)

    if doc.tags:
      current_tags = list(doc.tags)
    else:
      current_tags = []

    current_tags.append(category)
    current_tags_set = set(current_tags)
    doc.update(using=client,index=index,tags=list(current_tags_set))

    print(f'{index} - doc ({id}): updated')


for element in elements:
  q = query.get_topic_query(element, None, index)
  r = query.run_query(index, q)
  hits = query.process_response(r)
  for id in hits:
    if index == 'projects':
      doc = Project.get(using=client, index=index, id=id)
    elif index == 'publications':
      doc = Publication.get(using=client, index=index, id=id)

    if doc.element_tags:
      current_tags = list(doc.element_tags)
    else:
      current_tags = []

    current_tags.append(element)
    current_tags_set = set(current_tags)
    doc.update(using=client,index=index,element_tags=list(current_tags_set))

    print(f'{index} - doc ({id}): updated')




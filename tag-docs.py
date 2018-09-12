from elasticsearch_dsl import Q
from elastic import client, query
from elastic.models import Project
from StrategicResearch.elasticapp.queries import get_query

categories = ['construction_quality','design_and_details','material_specifications',
    'live_load', 'environment', 'maintenance_and_preservation',
    'structural_integrity', 'structural_condition', 'functionality', 'cost'
  ]

index='projects'

def remove_tags(index):
  q = query.Q({"match_all": {}})
  r = query.run_query(index, q)
  hits = query.process_response(r)

  for id in hits:
    doc = Project.get(using=client, index=index, id=id)
    doc.update(using=client,index=index,tags=list())
    print(f'Doc ({id}): updated')
    
remove_tags(index)

for category in categories:
  q = get_query(category)
  r = query.run_query(index, q)
  hits = query.process_response(r)
  for id in hits:
    # print(hit.id)
    doc = Project.get(using=client, index=index, id=id)
    if doc.tags:
      current_tags = list(doc.tags)
    else:
      current_tags = []
    current_tags.append(category)
    current_tags_set = set(current_tags)
    doc.update(using=client,index=index,tags=list(current_tags_set))
    print(f'Doc ({id}): updated')





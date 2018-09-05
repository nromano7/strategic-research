from elasticsearch_dsl import Q
from elastic import client, query
from elastic.models import Project

q = Q(
  {
    "bool": {
      "must": [
        {
          "bool": {
            "should": [
              {"match": {"title":"construction"}},
              {"match": {"abstract":"construction"}}
            ]
          }
        }
      ],
      "should": [
        {"match":{"title":"quality"}},
        {"match":{"abstract":"quality"}},
        {"match":{"title.bigram":"construction quality"}},
        {"match":{"abstract.bigram":"construction quality"}}
      ]
    }
  }
)

index = 'projects'
tag = 'construction quality'
r = query.run_query(index, q)
hits = query.process_response(r)
for id in hits:
  doc = Project.get(using=client, index=index, id=id)
  if doc.tags:
    current_tags = list(doc.tags)
  else:
    current_tags = []
  current_tags.append(tag)
  current_tags_set = set(current_tags)
  doc.update(using=client,index=index,tags=list(current_tags_set))
  print(f'Doc ({id}): updated')


def remove_tags(index):
  q = query.Q({"match_all": {}})
  r = query.run_query(index, q)
  hits = query.process_response(r)

  for id in hits:
    doc = Project.get(using=client, index=index, id=id)
    doc.update(using=client,index=index,tags=list())
    print(f'Doc ({id}): updated')



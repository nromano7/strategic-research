from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
from pytools.ContextManagers.timer import timer

query = "admixtures"

index = 'projects'
doc_type = 'doc'
client = Elasticsearch()
s = Search(using=client,index=index)

with timer('match'):
  q = Q({"match":{"abstract": query}})
  r = s.query(q)
  print(f'Hits: {r.count()}')

with timer('match_phrase'):
  q = Q({"match_phrase":{"abstract": query}})
  r = s.query(q)
  print(f'Hits: {r.count()}')

with timer('multi_match: best_fields'):
  q = Q(
    {
      "multi_match":{
        "query": query,
        "type":"best_fields",
        "fields":["title","abstract"]
      }
    }
  )
  r = s.query(q)
  print(f'Hits: {r.count()}')

with timer('multi_match: most_fields'):
  q = Q(
    {
      "multi_match":{
        "query": query,
        "type":"most_fields",
        "fields":["title","abstract"]
      }
    }
  )
  r = s.query(q)
  print(f'Hits: {r.count()}')

with timer('multi_match: phrase'):
  q = Q(
    {
      "multi_match":{
        "query": query,
        "type":"phrase",
        "fields":["title","abstract"]
      }
    }
  )
  r = s.query(q)
  print(f'Hits: {r.count()}')

with timer('multi_match: cross_fields'):
  q = Q(
    {
      "multi_match":{ #In other words, all terms must be present in at least one field for a document to match.
        "query": query,
        "type":"cross_fields",
        "fields":["title","abstract"],
        "operator":"and"      }
    }
  )
  r = s.query(q)
  print(f'Hits: {r.count()}')


# with timer('simple_query_string'):
#   q = Q(
#     {
#       "simple_query_string":{
#         "query":"live-l*",
#         "analyze_wildcard":True,
#         "default_operator":"AND"
#       }
#     }
#   )
#   r = s.query(q)
#   print(f'Hits: {r.count()}')
#   print()
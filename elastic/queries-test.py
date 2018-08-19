from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search 
import queries

# TODO: test all functions in queries.py (validate in Kibana console)

AWS_EP = r"https://search-strategic-research-eqhxwqugitmyfpzyiobs2dadue.us-east-1.es.amazonaws.com"
client = Elasticsearch()
fields=["title","abstract"]
index='projects'

query="deck*"

def run_query(index, q):
  # initialize search object
  s = Search(using=client, index=index)
  # query and return the response
  r = s.query(q)
  return r

def process_response(r):
  # process documents returned by the search
  hits_count = r.count()
  hits = {}
  for h in r.scan():
    # get data from document fields
    doc_id = h.meta.id
    title = h.title
    abstract = h.abstract
    matched_queries = list(h.meta.matched_queries)
    score = h.meta.score
    # store documents returned by the search
    hits[doc_id] = dict(
      title = title,
      abstract = abstract,
      matched_queries = matched_queries,
      score = score
    )
  return hits, hits_count

#  retrieve query object
must = dict(wildcard=[("title",query),("abstract",query)])
must_not = dict(match=[("title","overlay"),("abstract","overlay")])
q = queries.bool_query(must=must, must_not=must_not)

# run query and process response
r = run_query(index, q)
hits, hits_count = process_response(r)

print(f"[Total hits for query: '{query}'] {hits_count}")

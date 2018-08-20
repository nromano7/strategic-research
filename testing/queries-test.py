from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search 
import queries 

# TODO: test all functions in queries.py (validate in Kibana console)

client = Elasticsearch()
index='projects'

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

# match query on single field
query = "deck"
field = "title"
q = queries.match(query, field)
r = run_query(index, q)
hits, hits_count = process_response(r)

assert hits_count==136

# multi_match query  
query = "deck"
fields = ["title","abstract"]
q = queries.multimatch(query, fields)
r = run_query(index, q)
hits, hits_count = process_response(r)

assert hits_count==273

# bool query with must
must = dict(wildcard=[("title","deck"),("abstract","deck")])
q = queries.boolean(must=must)
r = run_query(index, q)
hits, hits_count = process_response(r)

assert hits_count==121

# bool query with must_not
must = dict(wildcard=[("title","deck"),("abstract","deck")])
must_not = dict(match=[("title","overlay"),("abstract","overlay")])
q = queries.boolean(must=must, must_not=must_not)
r = run_query(index, q)
hits, hits_count = process_response(r)

assert hits_count==92

print("all tests passed.")

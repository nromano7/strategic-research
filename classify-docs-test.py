from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search 
from elastic import queries 
import itertools 

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

# find documents that match "deck"
query = "deck"
prefixes = ["bridge","concrete","reinforced"]
fields = ["title","abstract"]

# TODO: write function to construct should statements 
# given query/prefixes, fields and for associated terms
# TODO: test approaches (with and without prefixes, associated terms)
should = dict(match=[("title",query),("abstract",query)])

q = queries.boolean(should=should)
r = run_query(index, q)
hits, hits_count = process_response(r)
print(f"[should (title,abstract: {query})]: {hits_count}")


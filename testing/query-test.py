from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q

# initialize elastic search client and search object
AWS_EP = r"https://search-strategic-research-eqhxwqugitmyfpzyiobs2dadue.us-east-1.es.amazonaws.com"
client = Elasticsearch()

def run_query(index, q, fields=["title","abstract"], doc_type='doc'):
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

# construct the query
q = Q(
  {
    "match": {
      "title": {
        "query": "deck",
        "_name": "title:deck"
      }
    }
  }
)

# run query and process respoinse
r = run_query('projects', q)
hits, hits_count = process_response(r)


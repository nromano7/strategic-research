
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, Q
import argparse
from queries import construct_query

AWS_EP = r"https://search-strategic-research-eqhxwqugitmyfpzyiobs2dadue.us-east-1.es.amazonaws.com"

# parse input arguments
parser = argparse.ArgumentParser(
  prog = __file__.split(".")[0], 
  description = "Interface for querying index in elasticsearch."
  )
parser.add_argument('-c', "--client", metavar='', type=str, help='the elasticsearch client')
parser.add_argument('-i', "--index", metavar='', type=str, required=True, help='the index to query')
parser.add_argument('-q', "--query", metavar='', type=str, required=True, help='the query to execute')
args = parser.parse_args()

# initialize elastic search client
if args.client == 'AWS':
  client = Elasticsearch(AWS_EP)
else:
  client = Elasticsearch()

# unpack arguments
query = args.query
index = args.index

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

#  retrieve query object
q = construct_query(query)

# run query and process response
r = run_query('projects', q)
hits, hits_count = process_response(r)

print(f"[Total hits for query: '{query}'] {hits_count}")

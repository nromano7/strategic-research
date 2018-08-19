import argparse
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search 
import queries as query

AWS_EP = r"https://search-strategic-research-eqhxwqugitmyfpzyiobs2dadue.us-east-1.es.amazonaws.com"

# parse input arguments
parser = argparse.ArgumentParser(
  prog = __file__.split(".")[0], 
  description = "Interface for querying index in elasticsearch."
)
parser.add_argument('-c', "--client", metavar='', type=str, help='the elasticsearch client')
parser.add_argument('-i', "--index", metavar='', type=str, required=True, help='the index to query')
parser.add_argument('-q', "--query", metavar='', type=str, required=True, help='the query to execute')
parser.add_argument('-f', "--fields", metavar='', type=str, help='the set of fields to query')
args = parser.parse_args()

# initialize elastic search client
if args.client == 'AWS':
  client = Elasticsearch(AWS_EP)
else:
  client = Elasticsearch()

# get fields if provided
if not args.fields:
  fields=["title","abstract"]
else:
  fields = args.fields

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
should = {'match': [("title","deck"),("abstract","deck")]}
q = query.bool_query(should=should)

# run query and process response
r = run_query(args.index, q)
hits, hits_count = process_response(r)

print(f"[Total hits for query: '{args.query}'] {hits_count}")

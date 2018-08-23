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

# function that constructs should clause for queries and fields
def construct_bool_clause(queries, fields):
  all_queries=[]
  for query in queries:
    for field in fields:
      query_field = get_query_field(query, field)
      all_queries.append((query_field,query))
  should = dict(match=all_queries)
  return should

# function that returns a list of fields based on provided query
def get_query_field(query, field):
  n_terms = len(query.split(" "))
  if n_terms == 1:
    return field
  if n_terms == 2:
    return field + ".bigram"
  if n_terms == 3:
    return field + ".trigram"
  if n_terms == 4:
    return field + ".quadragram"
  if n_terms == 5:
    return field + ".pentagram"
  # otherwise
  return field

# function that constructs phrase from query term and prefixes
def construct_phrase_queries(query, prefixes):
  phrase_queries = []
  for prefix in prefixes:
    phrase_queries.append(f"{prefix} {query}")
  return phrase_queries

# TODO: test approaches (with and without prefixes, associated terms)

# find documents that match bridge elements
element_queries = ["deck", "joint", "bearing","girder", "beam"]
fields = ["title","abstract"]

for query in element_queries:
  should = construct_bool_clause([query], fields)
  q = queries.boolean(should=should)
  r = run_query(index, q)
  hits, hits_count = process_response(r)
  print(f"[{query}]: {hits_count}")

# try to separate document overlap
should=construct_bool_clause(["deck"],fields)
must_not=construct_bool_clause(["girder", "beam"],["title"])
q = queries.boolean(should=should, must_not=must_not)
r = run_query(index, q)
hits, hits_count = process_response(r)
print(f"[deck NOT (girder OR beam)]: {hits_count}")


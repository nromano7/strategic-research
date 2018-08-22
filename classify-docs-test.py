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
prefixes1 = ["bridge","concrete","reinforced"]
prefixes2 = ["concrete bridge","reinforced bridge"]
prefixes3 = ["reinforced concrete bridge"]
fields = ["title","abstract"]


# function that constructs should clause for queries and fields
def construct_should_clause(queries, fields):
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

# no prefixes
all_queries = [query]
should = construct_should_clause(all_queries, fields)
q = queries.boolean(should=should)
r = run_query(index, q)
hits, hits_count = process_response(r)
print(f"[should (title, abstract: {all_queries})]: {hits_count}")

# single prefixes
all_queries = construct_phrase_queries(query, prefixes1)
should = construct_should_clause(all_queries, fields)
q = queries.boolean(should=should)
r = run_query(index, q)
hits, hits_count = process_response(r)
print(f"[should (title, abstract: {all_queries})]: {hits_count}")

# double prefixes
all_queries = construct_phrase_queries(query, prefixes2)
should = construct_should_clause(all_queries, fields)
q = queries.boolean(should=should)
r = run_query(index, q)
hits, hits_count = process_response(r)
print(f"[should (title, abstract: {all_queries})]: {hits_count}")

# triple prefixes
all_queries = construct_phrase_queries(query, prefixes3)
should = construct_should_clause(all_queries, fields)
q = queries.boolean(should=should)
r = run_query(index, q)
hits, hits_count = process_response(r)
print(f"[should (title, abstract: {all_queries})]: {hits_count}")





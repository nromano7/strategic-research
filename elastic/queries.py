from elasticsearch_dsl import Q

# TODO: update functions to allow for combinations of queries 
# and fields...{field:query}
# TODO finish multi_match query

def match_query(query, field, name='match'):
  """
  Return 'match' query object for the provided
  query and field.

  Parameters
  ----------
  query : str The provided query string.
  field : str The field to be queried.
  name  : str A name given to the query.

  Returns
  -------
  A query object for the provided query and field.

  """
  q = Q(
    {
      "match": {
        f"{field}": {
          "query": query,
          "_name": f"[{name}]{field}:{query}"
        }
      }
    }
  )

  return q

def wildcard_query(query, field, name='wildcard'):
  """
  Return 'wildcard' query object for the provided
  query and field. 

  Parameters
  ----------
  query : str The provided query string.
  field : str The field to be queried.
  name  : str A name given to the query.

  Returns
  -------
  A query object for the provided query and field.

  """
  q = Q(
    {
      "wildcard": {
        f"{field}": {
          "query": query,
          "_name": f"[{name}]{field}:{query}"
        }
      }
    }
  )

  return q

def bool_query(must={}, should={}, must_not={}):
  """
  Return 'bool' query object for the provided 'must',
  'should', and 'must_not' queries. 
  
  'must' query clauses but do not match the 'must_not' 
  query clauses. 'should' query clauses only affect the
  relevce score of the document (i.e. the ordering
  of the documents returned).

  Parameters
  ----------
  must      : dict 
    Dictionary of queries that must appear in the provided 
    field(s) in the form of {field:query}.
  should    : dict 
    Dictionary of queries that should appear in the provided 
    field(s) in the form of {field:query}.
  must_not  : dict 
    Dictionary of queries that must not appear in the 
    provided field in the form of {field:query}.

  Returns
  -------
  A query object for the provided queries and field(s).

  """
  # construct must clause for every field
  must_clauses = []
  for field, query in must:
    must_clauses.append(match_query(query,field,name='must'))
  # construct should clause for every field
  should_clauses = []
  for field, query in should:
    should_clauses.append(match_query(query,field,name='should'))
  # construct must_not clause for every field
  not_clauses = []
  for field, query in must_not:
    not_clauses.append(match_query(query,field,name='not'))
  
  q = Q(
    {
      "bool": {
        "must": must_clauses,
        "should": should_clauses,
        "must_not": not_clauses
      } 
    }
  )

  return q

def multimatch_query(query, fields):
  # construct should clause for every field
  # should_clauses = []
  # for field in fields:
  #   should_clauses.append(match_query(query,field))

  # this bool query is equivalent to the multi_match query for most_fields
  q = bool_query(must={}, should={}, must_not={})

  return q



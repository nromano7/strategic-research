from elasticsearch_dsl import Q

def match(query, field, name='match'):
  """
  Return 'match' query object for the provided
  query and field. 

  Parameters
  ----------
  query : str 
    The provided query string.
  field : str 
    The field to be queried.
  [name] : str
    A name given to the query.

  Returns
  -------
  A query object for the provided query and field.

  """
  # construct the query
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


def wildcard(query, field, name='wildcard'):
  """
  Return 'wildcard' query object for the provided
  query and field. 

  Parameters
  ----------
  query : str 
    The provided query string.
  field : str 
    The field to be queried.
  [name] : str 
    A name given to the query.

  Returns
  -------
  A query object for the provided query and field.

  """
  # construct the query
  q = Q(
    {
      "wildcard": {
        f"{field}": {
          "value": query,
          "_name": f"[{name}]{field}:{query}"
        }
      }
    }
  )

  return q


def get_query_func(query_type):
  """
  Return query function for provided query_type. 

  Parameters
  ----------
  query_type : str 
    The provided query type.

  Returns
  -------
  A query function for the provided query type.
  """
  query_functions = {
    "match": match,
    "wildcard": wildcard,
  }
  return query_functions.get(query_type)


def boolean(must=None, should=None, must_not=None):
  """
  Return 'bool' query object for the provided 'must',
  'should', and 'must_not' queries. 
  
  'must' queries require a document to match the query in 
  the provided field for the specified query type.

  'must_not' queries exclude documenta that match the query 
  in the provided field for the specified query type.
  
  'should' queries only affect the relevance score of the 
  matched documents (i.e. the ordering of the documents returned).

  Parameters
  ----------
  must      : dict 
    Dictionary in the form of {type:[(field,query),...]} for
    queries that must match in the provided field for the
    specified query type.
  should    : dict 
    Dictionary in the form of {type:[(field,query),...]} for
    queries that must match in the provided field for the
    specified query type.
  must_not  : dict 
    Dictionary in the form of {type:[(field,query),...]} for
    queries that must match in the provided field for the
    specified query type.

  Returns
  -------
  A query object for the provided queries and field(s).

  """
  def get_bool_queries(clause, name):
    # example input: clause=dict(type=[(field,query),...])
    queries = []
    if clause is not None:
      # construct list of boolean clauses
      for query_type in clause.keys():
        query_func = get_query_func(query_type)
        for field, query in clause.get(query_type):
          queries.append(query_func(query, field, name=name))
    return queries

  # get must queries
  must_clauses = get_bool_queries(must, 'must')
  # get should queries
  should_clauses = get_bool_queries(should, 'should')
  # get must_not queries 
  not_clauses = get_bool_queries(must_not, 'must_not')

  # construct the query
  q = Q("bool",
    must=must_clauses,
    should=should_clauses,
    must_not=not_clauses
  )

  return q


def multimatch(query, fields, query_type='match'):
  """
  Return 'multi_match' query object for the provided query 
  and list of fields. 

  Parameters
  ----------
  query : str
    The provided query string.
  fields : list  
    The list of fields to be queried.
  [query_type] : str   
    The default query type.

  Returns
  -------
  A query object for the provided queries and field(s).
  """
  # check if wildcard query is needed
  if "*" in query:
    query_type='wildcard'
  
  # construct 'should' data strucutre 
  should = {query_type: []}
  for field in fields:
    should[query_type].append((field,query))

  # this bool query is equivalent to the multi_match query 
  # with a most_fields type
  q = boolean(should=should)

  return q



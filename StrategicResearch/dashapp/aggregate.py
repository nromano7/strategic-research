from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, A, Q

client = Elasticsearch()
index = 'projects'

def project_count_by_state(query=None):

  # search object
  s = Search(using=client,index=index)

  if query:

    # fields to query
    fields = ["title","abstract","notes","TRID_INDEX_TERMS","TRID_SUBJECT_AREAS",'tags']
    
    q=Q(
      {
        "multi_match":{
          "query": query,
          "type":"best_fields",
          "fields":fields
        }
      }
    )
    s=s.query(q)

  # aggregations
  a1 = A(
    "nested", 
    path="funding_agencies"
  )
  a2 = A(
    "terms", 
    field="funding_agencies.state.keyword",
    size=50, 
    order={"_count": "desc"}
  )

  # chain aggregations and execute
  s.aggs\
    .bucket('agencies', a1)\
    .bucket('states',a2)
  response = s.execute()

  # filter response
  res = {}
  for b in response.aggregations.agencies.states.buckets:
    state = b['key']
    doc_count = b['doc_count']
    res[state] = doc_count
  
  return res

def project_count(query=None):

  # search object
  s = Search(using=client,index=index)

  # fields to query
  fields = ["title","abstract","notes","TRID_INDEX_TERMS","TRID_SUBJECT_AREAS",'tags']
  allStatus = ['Active', 'Completed', 'Programmed', 'Proposed']

  if query:

    if query == 'all':
      q=Q({"match_all":{}})
    else:
      q=Q({"match":{"tags":query}})

    s=s.query(q)
    res={}
    res['total'] = s.count()
    for status in allStatus:
      res[status.lower()] = s.filter("match",status=status).count()

  else:

    # query
    total = Q(
      {
        "match_phrase": {
          "doc_type": {
            "query": "project"
          }
        }
      }
    )
    s=s.query(total)
    res={}
    res['total'] = s.count()
    for status in allStatus:
      q = Q(
        {
          "match_phrase": {
            "status.keyword": {
              "query": status
            }
          }
        }
      )
      res[status.lower()] = s.query(q).count()

  return res

def project_count_by_tag(tag):

  # search object
  s = Search(using=client,index=index)

  # construct query
  q = Q({"match":{"tags": tag}})
  s = s.query(q)

  count = s.count()

  return count

def publication_count(query=None):

   # search object
  s = Search(using=client,index='publications')
  
  fields = ["title","abstract","notes","TRID_INDEX_TERMS","TRID_SUBJECT_AREAS",'tags']

  if query:

    if query == "all":
      q=Q({"match_all":{}})
    else:
      q=Q({"match":{"tags":query}})

    count = s.query(q).count()

  else:

    # query
    total = Q(
      {
        "match_phrase": {
          "doc_type": {
            "query": "publication"
          }
        }
      }
    )

    count = s.query(total).count()

  return count

  
def funding_by_state(query=None):

  # search object
  s = Search(using=client,index=index)

  if query:

    # fields to query
    fields = ["title","abstract","notes","TRID_INDEX_TERMS","TRID_SUBJECT_AREAS",'tags']
    
    q=Q(
      {
        "multi_match":{
          "query": query,
          "type":"best_fields",
          "fields":fields
        }
      }
    )
    s=s.query(q)

  # aggregations
  a1 = A(
    "nested", 
    path="funding_agencies"
  )
  a2 = A(
    "terms", 
    field="funding_agencies.state.keyword",
    size=50, 
    order={"_count":"desc"},
  )
  a3 = A("reverse_nested")
  a4 = A(
    "range", 
    field="funding", 
    ranges=[
      {
        "from": 0, "to": 100000
      },
      {
        "from": 100000,"to": 250000
      },
      {
        "from": 250000,"to": 500000
      },
      {
        "from": 500000,"to": 750000
      },
      {
        "from": 750000,"to": 1000000
      },
      {
        "from": 1000000
      }
    ],
    keyed=True
  )

  # chain aggregations and execute
  s.aggs\
    .bucket('agencies', a1)\
    .bucket('states',a2)\
    .bucket('reverse',a3)\
    .bucket('fund_amt',a4)
  response = s.execute()

  # filter response
  res = {}
  for b in response.aggregations.agencies.states.buckets:
    state = b.key
    buckets = b.reverse.fund_amt.buckets.to_dict()
    res[state] = buckets
  
  return res

from app import client
from elasticsearch_dsl import Search, A, Q
import json

index = 'projects'
doc_type = 'doc'

def FundingLevelByState(query=None):

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

def ProjectCountByState(query=None):

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

def FundingByYear(query=None):
  
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
    "date_range", 
    field="actual_complete_date",
    ranges=[
      {
        "from": "2013-01-01",
        "to": "2014-01-01"
      },
      {
        "from": "2014-01-01",
        "to": "2015-01-01"
      },
      {
        "from": "2015-01-01",
        "to": "2016-01-01"
      },
      {
        "from": "2016-01-01",
        "to": "2017-01-01"
      },
      {
        "from": "2017-01-01",
        "to": "2018-01-01"
      },
      {
        "from": "2018-01-01",
        "to": "2019-01-01"
      }
    ]
  )
  a2 = A(
    "sum",
    field='funding'
  )
  
  # chain aggregations and execute
  s.aggs\
    .bucket('dateRange', a1)\
    .metric('sumFunding',a2)
  response = s.execute()

  # filter response
  res = {}
  for bucket in list(response.aggregations.dateRange.buckets):
    year = bucket.key[:4] # year only
    res[year] = bucket.sumFunding.value
  
  return res

def ProjectCountByYear(query=None):
  
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
    "date_range", 
    field="actual_complete_date",
    ranges=[
      {
        "from": "2013-01-01",
        "to": "2014-01-01"
      },
      {
        "from": "2014-01-01",
        "to": "2015-01-01"
      },
      {
        "from": "2015-01-01",
        "to": "2016-01-01"
      },
      {
        "from": "2016-01-01",
        "to": "2017-01-01"
      },
      {
        "from": "2017-01-01",
        "to": "2018-01-01"
      },
      {
        "from": "2018-01-01",
        "to": "2019-01-01"
      }
    ]
  )
  
  # chain aggregations and execute
  s.aggs\
    .bucket('dateRange', a1)
  response = s.execute()

  # filter response
  res = {}
  for bucket in list(response.aggregations.dateRange.buckets):
    year = bucket.key[:4]
    res[year] = bucket.doc_count
  
  return res

def ProjectCount(query=None):

  # search object
  s = Search(using=client,index=index)

  # fields to query
  fields = ["title","abstract","notes","TRID_INDEX_TERMS","TRID_SUBJECT_AREAS",'tags']
  allStatus = ['Active', 'Completed', 'Programmed', 'Proposed']

  if query:

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

def PublicationCount(query=None):

  # search object
  s = Search(using=client,index='publications')
  
  fields = ["title","abstract","notes","TRID_INDEX_TERMS","TRID_SUBJECT_AREAS",'tags']

  if query:

    q=Q(
      {
        "multi_match":{
          "query": query,
          "type":"best_fields",
          "fields":fields
        }
      }
    )
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

def LTBPTermsCount():
  s = Search(using=client,index=index)

  inAttr = [
    "Construction",
    "Design",
    "Environment",
    "Live Load",
    "Maintenance & Preservation",
    "Material"
  ]
  fields = ["title","abstract","notes","TRID_INDEX_TERMS","TRID_SUBJECT_AREAS", "tags"]

  res={}
  for i in inAttr:
    q = Q(
      {
        "multi_match":{
          "query": i,
          "type":"best_fields",
          "fields": fields
        }
      }
    )
    res[i] = s.query(q).count()

  return res

# res = ProjectCountByYear()
# print()
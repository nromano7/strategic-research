from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, A, Q
import json

index = 'projects'
doc_type = 'doc'
client = Elasticsearch()

def FundingLevelByState():
  # search object
  s = Search(using=client,index=index)

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
  a3 = A("reverse_nested")
  a4 = A(
    "range", 
    field="funding", 
    ranges=[
      {
        "from": 0,
        "to": 100000
      },
      {
        "from": 100000,
        "to": 250000
      },
      {
        "from": 250000,
        "to": 500000
      },
      {
        "from": 500000,
        "to": 750000
      },
      {
        "from": 750000,
        "to": 1000000
      },
      {
        "from": 1000000
      }
    ],
    keyed=True
  )

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

def ProjectCountByState():
  # search object
  s = Search(using=client,index=index)

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

def FundingByYear():
  # search object
  s = Search(using=client,index=index)

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
  
  s.aggs\
    .bucket('dateRange', a1)\
    .metric('sumFunding',a2)

  response = s.execute()

  # filter response
  res = {}
  for bucket in list(response.aggregations.dateRange.buckets):
    year = bucket.key[:4]
    res[year] = bucket.sumFunding.value
  
  return res

def ProjectCount():
  # search object
  s = Search(using=client,index=index)

  # query
  total = Q(
    {
      "match_phrase": {
        "type": {
          "query": "project"
        }
      }
    }
  )
  active = Q(
    {
      "match_phrase": {
        "status.keyword": {
          "query": "Active"
        }
      }
    }
  )
  complete = Q(
    {
      "match_phrase": {
        "status.keyword": {
          "query": "Completed"
        }
      }
    }
  )
  programmed = Q(
    {
      "match_phrase": {
        "status.keyword": {
          "query": "Programmed"
        }
      }
    }
  )
  proposed = Q(
    {
      "match_phrase": {
        "status.keyword": {
          "query": "Proposed"
        }
      }
    }
  )

  res=dict(
    total=s.query(total).count(),
    active=s.query(active).count(),
    complete=s.query(complete).count(),
    programmed=s.query(programmed).count(),
    proposed=s.query(proposed).count()
  )

  return res

def PublicationCount():

  # search object
  s = Search(using=client,index='publications')

  # query
  total = Q(
    {
      "match_phrase": {
        "type": {
          "query": "publication"
        }
      }
    }
  )

  count = s.query(total).count()

  return count

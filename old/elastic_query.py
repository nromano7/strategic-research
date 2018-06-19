import json
from elasticsearch import Elasticsearch
from pytools.ContextManagers.timer import timer

with open('./files/heatmap_res.json', 'r') as f:
  res = json.load(f)

states = res['aggregations']['agencies']['states']['buckets']
states = [state for state in states if state.get('key') != 'DC'] # remove DC
X = []
Y = ['0.0-100000.0','100000.0-250000.0','250000.0-500000.0','500000.0-750000.0','750000.0-1000000.0']
# y = ["$<100k", "$100-250k", "$250-500k", "$500-750k", "$750k-1M", "$1M+"]
Z = []
count = 0
for state in states:
  count += 1
  if count > 5:
    break
  X.append(state.get('key'))
  z = []
  for fRange in Y:
    z.append(state['reverse']['fund_amt']['buckets'][fRange]['doc_count'])
  Z.append(z)

es = Elasticsearch()

# with timer('loading json took'):
# 	with open('./files/heatmap_agg.json', 'r') as f:
# 		doc = json.load(f)
doc = {
  "size": 0,
  "_source": {
    "excludes": []
  },
  "aggs": {
    "2": {
      "terms": {
        "field": "funding_agencies.state.keyword",
        "size": 50,
        "order": {
          "_count": "desc"
        }
      },
      "aggs": {
        "3": {
          "range": {
            "field": "funding",
            "ranges": [
              {
                "from": 0,
                "to": 99999
              },
              {
                "from": 100000,
                "to": 249999
              },
              {
                "from": 250000,
                "to": 499999
              },
              {
                "from": 500000,
                "to": 749999
              },
              {
                "from": 750000,
                "to": 999999
              },
              {
                "from": 1000000,
                "to": 1249999
              },
              {
                "from": 1250000,
                "to": 10000000
              }
            ],
            "keyed": true
          }
        }
      }
    }
  },
  "version": true,
  "stored_fields": [
    "*"
  ],
  "script_fields": {},
  "docvalue_fields": [
    "actual_complete",
    "expected_complete",
    "publication_date",
    "start"
  ],
  "query": {
    "bool": {
      "must": [
        {
          "match_all": {}
        },
        {
          "match_all": {}
        }
      ],
      "filter": [],
      "should": [],
      "must_not": [
        {
          "match_phrase": {
            "funding_agencies.state.keyword": {
              "query": "DC"
            }
          }
        }
      ]
    }
  }
}

with timer('localhost search'):
	res = es.search(index="trid-projects", body=doc)
	print("Got %d Hits:" % res['hits']['total'])
	# for hit in res['hits']['hits']:
	#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])


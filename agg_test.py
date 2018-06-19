from elasticsearch import Elasticsearch
from elasticsearch_dsl import A, Search
import json

index = 'projects'
doc_type = 'doc'
client = Elasticsearch()

s = Search(using=client,index=index)
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

s.aggs.bucket('agencies', a1).bucket('states',a2).bucket('reverse',a3).bucket('fund_amt',a4)

res = s.execute()

# print(json.dumps(s.to_dict(),indent=1))
print(json.dumps(res.aggregations.agencies.states,indent=1))


# NestedFacet("funding_agencies",TermsFacet(field="funding_agencies.state.keyword")

{
  "size":0,
  "aggs": {
    "agencies": {
      "nested":{"path":"funding_agencies"},
      "aggs": {
        "states":{
          "terms": {
            "field": "funding_agencies.state.keyword",
            "size": 50,
            "order": {"_count": "desc"}
          },
          "aggs": {
            "reverse": {
              "reverse_nested": {},
              "aggs": {
                "fund_amt": {
                  "range": {
                    "field": "funding",
                    "ranges": [
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
                    "keyed": true
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
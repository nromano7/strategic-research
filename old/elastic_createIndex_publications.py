from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient

index = 'publications'
mapping = {
  "mappings":{
    "_doc": {
      "properties": {
        "type": {"type":"keyword"},
        "title": {"type":"text"},
        "abstract": {"type":"text"},
        "notes": {"type":"text"},
        "urls": {"type":"text"},
        "authors": {
          "type":"nested",
          "properties": {
            "first_name":{"type":"keyword"},
            "last_name":{"type":"keyword"},
            "position":{"type":"integer"}
          }
        },
        "serial":{"type":"text"},
        "serial_url":{"type":"text"},
        "publisher":{"type":"text"},
        "publication_date":{
          "type":"date",
          "format":"yyyy-MM-dd"
        },
        "TRID_RECORD_BASE": {"type":"text"},
        "TRID_RECORD_ID": {"type":"keyword"},
        "TRID_RECORD_TYPE": {"type":"keyword"},
        "TRID_TRIS_FILE_CODES": {"type":"keyword"},
        "TRID_INDEX_TERMS": {"type":"keyword"},
        "TRID_SUBJECT_AREAS": {"type":"keyword"}
      }
    }
  }
}

esClient = Elasticsearch()
indClient = IndicesClient(esClient)
res = indClient.create(
  index = index,
  body = mapping
)

print(res)

def getMapping():
  mapping = {
    "mappings": {
      "_doc": {
        "properties": {
          "TRID_INDEX_TERMS": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "TRID_RECORD_BASE": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "TRID_RECORD_ID": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "TRID_RECORD_TYPE": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "TRID_SUBJECT_AREAS": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "TRID_TRIS_FILE_CODES": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "abstract": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "authors": {
            "properties": {
              "first_name": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                  }
                }
              },
              "last_name": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                  }
                }
              },
              "position": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword",
                    "ignore_above": 256
                  }
                }
              }
            }
          },
          "notes": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "publication_date": {
            "type": "date"
          },
          "publisher": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "serial": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "serial_url": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "title": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          },
          "type":{
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          }
          "urls": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword",
                "ignore_above": 256
              }
            }
          }
        }
      }
    }
  }

  return mapping
def getProjectsMapping():
  mapping = {
  "mappings": {
      "_doc": {
        "properties": {
          "TRID_INDEX_TERMS": {
            "type": "nested",
            "properties":{
              "term": {
                "type":"text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              }
            }
          },
          "TRID_RECORD_BASE": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "TRID_RECORD_ID": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "TRID_RECORD_TYPE": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "TRID_SUBJECT_AREAS": {
            "type": "nested",
            "properties":{
              "subject_area": {
                "type":"text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              }
            }
          },
          "TRID_TRIS_FILE_CODES": {
            "type": "nested",
            "properties":{
              "tris_file": {
                "type":"text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              }
            }
          },
          "abstract": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "actual_complete": {
            "type": "date",
            "format":"yyyy-MM-dd"
          },
          "expected_complete": {
            "type": "date",
            "format":"yyyy-MM-dd"
          },
          "funding": {
            "type": "float"
          },
          "funding_agencies": {
            "type": "nested",
            "properties": {
              "city": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "country": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "name": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "postal_code": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "site_url": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "state": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              }
            }
          },
          "managing_agencies": {
            "type": "nested",
            "properties": {
              "city": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "country": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "name": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "postal_code": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "site_url": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "state": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              }
            }
          },
          "notes": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "performing_agencies": {
            "type": "nested",
            "properties": {
              "city": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "country": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "name": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "postal_code": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "site_url": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "state": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              }
            }
          },
          "project_investigators": {
            "type":"nested",
            "properties": {
              "firstname": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "lastname": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              }
            }
          },
          "responsible_individuals": {
            "type":"nested",
            "properties": {
              "firstname": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "lastname": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              }
            }
          },
          "start": {
            "type": "date",
            "format":"yyyy-MM-dd"
          },
          "status": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "title": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "type": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "urls": {
            "type": "nested",
            "properties":{
              "url": {
                "type":"text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              }
            }
          }
        }
      }
    }
  }
  return mapping

def getPublicationsMapping():
  mapping = {
    "mappings": {
      "_doc": {
        "properties": {
          "TRID_INDEX_TERMS": {
            "type": "nested",
            "properties":{
              "term": {
                "type":"text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              }
            }
          },
          "TRID_RECORD_BASE": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "TRID_RECORD_ID": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "TRID_RECORD_TYPE": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "TRID_SUBJECT_AREAS": {
            "type": "nested",
            "properties":{
              "subject_area": {
                "type":"text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              }
            }
          },
          "TRID_TRIS_FILE_CODES": {
            "type": "nested",
            "properties":{
              "tris_file": {
                "type":"text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              }
            }
          },
          "abstract": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "authors": {
            "type":"nested",
            "properties": {
              "first_name": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "last_name": {
                "type": "text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              },
              "position": {
                "type": "integer"
              }
            }
          },
          "notes": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "publication_date": {
            "type": "date",
            "format":"yyyy-MM-dd"
          },
          "publisher": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "serial": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "serial_url": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "title": {
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "type":{
            "type": "text",
            "fields": {
              "keyword": {
                "type": "keyword"
              }
            }
          },
          "urls": {
            "type": "nested",
            "properties":{
              "url": {
                "type":"text",
                "fields": {
                  "keyword": {
                    "type": "keyword"
                  }
                }
              }
            }
          }
        }
      }
    }
  }

  return mapping

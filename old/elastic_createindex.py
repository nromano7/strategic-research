from elasticsearch import Elasticsearch
from elasticsearch.client import IndicesClient
from elastic_mapping import getProjectsMapping, getPublicationsMapping
import sys

def createIndex(index,mapping):
  esClient = Elasticsearch()
  indClient = IndicesClient(esClient)
  res = indClient.create(
    index = index,
    body = mapping
  )
  print(res)

if 'projects' in sys.argv:
  index = "projects"
  mapping = getProjectsMapping()  
  createIndex(index,mapping)
elif 'publications' in sys.argv:
  index = 'publications'
  mapping = getPublicationsMapping()
  createIndex(index,mapping)
else:
  raise(Exception('no arguments provided.'))


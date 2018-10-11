from elasticsearch import Elasticsearch
from elasticsearch_dsl import Index
import models
import sys

# initialize ES client
# AWS_EP = "https://search-strategic-research-67yfnme5nbl3c45vigirwnko4q.us-east-2.es.amazonaws.com"
client = Elasticsearch()

if 'projects' in sys.argv:
  # initialize projects index
  projects = Index('projects', using=client)
  # register a document with the index
  projects.document(models.Project)
  # delete the index, ignore if it doesn't exist
  projects.delete(ignore=404)
  # create the index in elasticsearch
  projects.create()

elif 'publications' in sys.argv:
  # initialize publications index
  publications = Index('publications', using=client)
  # register a document with the index
  publications.document(models.Publication)
  # delete the index, ignore if it doesn't exist
  publications.delete(ignore=404)
  # create the index in elasticsearch
  publications.create()

else:
  raise(Exception())






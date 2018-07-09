from elasticsearch import Elasticsearch
from elasticsearch_dsl import DocType, Date, Nested, Boolean, InnerDoc, Keyword, Text, Float, Integer

# AWS_EP = r"https://elastic:wigWgahDPGf7Kh2JetHvcf3x@6c09a7dc67e4408c93e1416ac9bbc629.us-east-1.aws.found.io:9243"
client = Elasticsearch()

class Agency(InnerDoc):
  name = Text(fields={'keyword': Keyword()})
  city = Text(fields={'keyword': Keyword()})
  state = Text(fields={'keyword': Keyword()})
  country = Text(fields={'keyword': Keyword()})
  postal_code = Text(fields={'keyword': Keyword()})
  site_url = Text(fields={'keyword': Keyword()})

class Person(InnerDoc):
  firstname = Text(fields={'keyword': Keyword()})
  lastname = Text(fields={'keyword': Keyword()})

class Author(Person):
  position = Integer()

class Record(DocType):
  TRID_INDEX_TERMS = Text(multi=True, fields={'keyword': Keyword(multi=True)})
  TRID_RECORD_BASE = Text(fields={'keyword': Keyword()})
  TRID_RECORD_ID = Text(fields={'keyword': Keyword()})
  TRID_RECORD_TYPE = Text(fields={'keyword': Keyword()})
  TRID_SUBJECT_AREAS = Text(multi=True, fields={'keyword': Keyword(multi=True)})
  TRID_TRIS_FILE_CODES = Text(multi=True, fields={'keyword': Keyword(multi=True)})
  abstract = Text(fields={'keyword': Keyword()})
  doc_type = Text(fields={'keyword': Keyword()})
  notes = Text(fields={'keyword': Keyword()})
  title = Text(fields={'keyword': Keyword()})
  tags = Text(multi=True, fields={'keyword': Keyword(multi=True)})
  urls = Text(multi=True)

class Project(Record):
  actual_complete_date = Date(format='yyyy-MM-dd')
  expected_complete_date = Date(format='yyyy-MM-dd')
  funding = Float()
  funding_agencies = Nested(Agency)
  managing_agencies = Nested(Agency)
  performing_agencies = Nested(Agency)
  project_investigators = Nested(Person)
  responsible_individuals = Nested(Person)
  start_date = Date(format='yyyy-MM-dd')
  status = Text(fields={'keyword': Keyword()})
  
  class Meta:
    index = 'projects'

class Publication(Record):
  authors = Nested(Author)
  publication_date = Date(format='yyyy-MM-dd')
  publisher = Text(fields={'keyword': Keyword()})
  serial = Text(fields={'keyword': Keyword()})
  
  class Meta:
    index = 'publications'

Project.init(using=client)
Publication.init(using=client)



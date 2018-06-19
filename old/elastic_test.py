from datetime import datetime
from elasticsearch import Elasticsearch
import json
from os import listdir
from pytools.ContextManagers.timer import timer

AWS_EP = r"https://elastic:wigWgahDPGf7Kh2JetHvcf3x@6c09a7dc67e4408c93e1416ac9bbc629.us-east-1.aws.found.io:9243"

es1 = Elasticsearch()
es2 = Elasticsearch(AWS_EP,verify_certs=True)

with timer('localhost search'):
    res = es1.search(index="trid-*", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total'])
    # for hit in res['hits']['hits']:
    #     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

with timer('cloud search'):
    res = es2.search(index="trid-*", body={"query": {"match_all": {}}})
    print("Got %d Hits:" % res['hits']['total'])
    # for hit in res['hits']['hits']:
    #     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])
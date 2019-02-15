# import sys
from datetime import datetime
import os
from elasticsearch import Elasticsearch

now = datetime.now()
year, month, day = now.year, now.month, now.day

if os.environ.get('ELASTICSEARCH_URL'):
    client = Elasticsearch(os.environ['ELASTICSEARCH_URL'])
else:
    client = Elasticsearch()

# PROJECT_FILES_PATH = r"C:\Users\nickp\OneDrive\Documents\work\projects\ltbp\strategic-research\data-files\20180803\json\projects"
# PUB_FILES_PATH = r"C:\Users\nickp\OneDrive\Documents\work\projects\ltbp\strategic-research\data-files\20180803\json\publications"

# PROJECT_FILES_PATH = os.getcwd() + f"./.data/{year:04}{month:02}{day:02}/json/projects"
# PUB_FILES_PATH = os.getcwd() + f"./.data/{year:04}{month:02}{day:02}/json/publications"
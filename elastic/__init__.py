# import sys
# import os
# sys.path.append(os.getcwd())

from elasticsearch import Elasticsearch

# AWS_EP = "https://search-strategic-research-67yfnme5nbl3c45vigirwnko4q.us-east-2.es.amazonaws.com"
client = Elasticsearch()

PROJECT_FILES_PATH = r"C:\Users\nickp\OneDrive\Documents\work\projects\ltbp\strategic-research\data-files\20180803\json\projects"
PUB_FILES_PATH = r"C:\Users\nickp\OneDrive\Documents\work\projects\ltbp\strategic-research\data-files\20180803\json\publications"
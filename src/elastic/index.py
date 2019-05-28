import sys
import os
# print(os.getcwd())
sys.path.append(os.getcwd())

import datetime
from elastic import client, models, query#, PROJECT_FILES_PATH, PUB_FILES_PATH
from elasticsearch_dsl import Index, Q
import json
import sys
import os


"""
index.py contains functions for creating an index, 
indexing documents, and updating documents for the
given index in Elasticsearch.

create_index(): 
	function for creating a new index in Elasticsearch

index_documents(): 
	function for indexing documents into Elasticsearch
	for the provided index.

tag_documents():
	function that tags documents within the provided
	index for a given set of terms.

python -m elastic.index

"""

def create_index(index_name):

	"""
	Create a new index in Elasticsearch. The new index will
	be identified by the value of 'index_name'.

	index_name: 
		name of index to insert documents. Valid
		arguments: projects, publications

	"""

	if index_name not in ['projects', 'publications', 'appdata']:
		raise(Exception(f"'{index_name}' is not a valid index name."))

	if index_name == 'projects':
		model = models.Project
	elif index_name == 'publications':
		model = models.Publication
	elif index_name == 'appdata':
		model = models.appdata
	else:
		raise(Exception)

	# initialize index
	idx = Index(index_name, using=client)
	# register a document with the index
	idx.document(model)
	# delete the index, ignore if it doesn't exist
	idx.delete(ignore=404)
	# create the index in elasticsearch
	idx.create()


def index_documents(index_name, path_to_json_files, 
		verbose=True, testing=False):

	"""
	Index raw json documents into Elasticsearch. 

	index_name: 
		name of index to insert documents. Valid
		arguments: projects, publications

	path_to_json_files:
		path to raw json files to be inserted 
		into the provided index
	"""

	if index_name not in ['projects', 'publications']:
		raise(Exception(f"'{index_name}' is not a valid index name."))

	DOC_TYPE = 'doc'
	count = 0
	all_json_files = os.listdir(path_to_json_files)

	for file in all_json_files:

		# for testing only
		count += 1
		if testing and count == 100:
			return

		id = file.split('_')[1].split('.')[0]
		json_file_path = os.path.join(path_to_json_files, file)

		# check if document already exists
		if not client.exists(index=index_name, doc_type=DOC_TYPE, id=id,):

			# for each json file open and index into Elasticsearch
			with open(json_file_path, 'r') as f:
				doc = json.load(f)
				res = client.index(index=index_name, 
					doc_type=DOC_TYPE, id=id, body=doc)
				if verbose:
					print(f'[{index_name} doc:{id}] {res["result"]}')
	
	
def tag_documents(index_name, topic_tags, element_tags, init=False):

	def process_hits(hits):
		for item in hits:
			id = item['_id']
			index_name = item["_index"]
			if index_name == 'projects':
				doc = models.Project.get(using=client, index=index_name, id=id)
			elif index_name == 'publications':
				doc = models.Publication.get(using=client, index=index_name, id=id)
			doc.update(using=client,index=index_name,request_timeout=20,
				tags=list(),element_tags=list())
			print(f'{index_name} - doc ({id}): tags removed')

	def remove_tags(index_name):

		# Init scroll by search
		data = client.search(
			index=index_name,
			doc_type='doc',
			scroll='2m',
			size=1000,
			body={"query":{"match_all": {}}}
		)

		# Get the scroll ID
		sid = data['_scroll_id']
		scroll_size = len(data['hits']['hits'])

		# Before scroll, process current batch of hits
		process_hits(data['hits']['hits'])

		while scroll_size > 0:

			data = client.scroll(scroll_id=sid, scroll='2m')

			# Process current batch of hits
			process_hits(data['hits']['hits'])

			# Update the scroll ID
			sid = data['_scroll_id']

			# Get the number of results that returned in the last scroll
			scroll_size = len(data['hits']['hits'])

	# if initializing or (reinitializing) remove all tags
	if init:
		remove_tags(index_name)

	# topic tags
	for tag in topic_tags:
		kwargs = query.get_query_arguments(tag)
		q = query.Query(**kwargs)
		s = query.run_query(q.query, index=index_name)

		# filter out documents that are already tagged or have had the current tag removed
		s = s.filter("bool",**{"must_not":{"term":{"tags":tag}}}) \
			 .filter("bool",**{"must_not":{"term":{"removed_tags":tag}}})

		hits, _ = query.process_search_response(s, last=s.count())
		for id in hits:
			if index_name == 'projects':
				doc = models.Project.get(using=client, index=index_name, id=id)
			elif index_name == 'publications':
				doc = models.Publication.get(using=client, index=index_name, id=id)

			if doc.tags:
				current_tags = list(doc.tags)
			else:
				current_tags = []

			current_tags.append(tag)
			current_tags_set = set(current_tags)
			doc.update(using=client,index=index_name,tags=list(current_tags_set))

			print(f'{index_name} - doc ({id}): updated with {tag}')

	# element tags
	for tag in element_tags:
		kwargs = query.get_query_arguments(tag)
		q = query.Query(**kwargs)
		s = query.run_query(q.query, index=index_name)

		# filter out documents that are already tagged or have had the current tag removed
		s = s.filter("bool",**{"must_not":{"term":{"tags":tag}}}) \
			 .filter("bool",**{"must_not":{"term":{"removed_tags":tag}}})
			 
		hits, _ = query.process_search_response(s, last=s.count())
		for id in hits:
			if index_name == 'projects':
				doc = models.Project.get(using=client, index=index_name, id=id)
			elif index_name == 'publications':
				doc = models.Publication.get(using=client, index=index_name, id=id)

			if doc.element_tags:
				current_tags = list(doc.element_tags)
			else:
				current_tags = []

			current_tags.append(tag)
			current_tags_set = set(current_tags)
			doc.update(using=client,index=index_name,element_tags=list(current_tags_set))

			print(f'{index_name} - doc ({id}): updated with {tag}')


if __name__ == '__main__':

	topic_tags = [
		'construction_quality','design_and_details','material_specifications',
		'live_load', 'environment', 'maintenance_and_preservation',
		'structural_integrity', 'structural_condition', 'functionality', 'cost'
	]
		
	element_tags = [
		'superstructure', 'untreated_deck', 'treated_deck', 'joints', 
		'bearings', 'coatings', 'prestressing'
	]

	tag_documents("projects", topic_tags, element_tags, init=False)

	# if os.environ.get('DATAPATH'):
	# 	PROJECT_FILES_PATH = os.path.join(os.environ.get('DATAPATH'),'json','projects')
	# 	PUB_FILES_PATH = os.path.join(os.environ.get('DATAPATH'),'json','publications')
	# else:
	# 	PROJECT_FILES_PATH = r"./.data/json/projects"
	# 	PUB_FILES_PATH = r"./.data/json/publications"

	# create_index("projects")
	# index_documents("projects", PROJECT_FILES_PATH)
	# tag_documents("projects", topic_tags, element_tags, init=True)

	# create_index("publications")
	# index_documents("publications", PUB_FILES_PATH)
	# tag_documents("publications", topic_tags, element_tags, init=True)

	# create_index("appdata")
	# today = str(datetime.date.today())
	# client.index(index='appdata', doc_type='doc', id=1, body={"last_update":today})





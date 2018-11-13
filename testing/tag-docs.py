from elastic import client
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q
import query
from models import Project, Publication
import sys

topic_tags = [
	'construction_quality','design_and_details','material_specifications',
	'live_load', 'environment', 'maintenance_and_preservation',
	'structural_integrity', 'structural_condition', 'functionality', 'cost'
]
	
element_tags = ['untreated_deck','treated_deck','joints','bearings', 'coatings','prestressing']


def remove_tags(index):
	q = Q({"match_all": {"_name":"match_all"}})
	s = query.run_query(q, index)
	hits, _ = query.process_search_response(s, last=s.count())

	for id in hits:
		if index == 'projects':
			doc = Project.get(using=client, index=index, id=id)
		elif index == 'publications':
			doc = Publication.get(using=client, index=index, id=id)

		doc.update(using=client,index=index,tags=list(),element_tags=list())
		print(f'{index} - doc ({id}): tags removed')


if __name__ == '__main__':
	
	index = 'projects'
	remove_tags(index)

	for tag in topic_tags:
		kwargs = query.get_query_arguments(tag)
		q = query.Query(**kwargs)
		s = query.run_query(q.query, index=index)
		hits, _ = query.process_search_response(s, last=s.count())
		for id in hits:
			if index == 'projects':
				doc = Project.get(using=client, index=index, id=id)
			elif index == 'publications':
				doc = Publication.get(using=client, index=index, id=id)

			if doc.tags:
				current_tags = list(doc.tags)
			else:
				current_tags = []

			current_tags.append(tag)
			current_tags_set = set(current_tags)
			doc.update(using=client,index=index,tags=list(current_tags_set))

			print(f'{index} - doc ({id}): updated with {tag}')


	for tag in element_tags:
		kwargs = query.get_query_arguments(tag)
		q = query.Query(**kwargs)
		s = query.run_query(q.query, index=index)
		hits, _ = query.process_search_response(s, last=s.count())
		for id in hits:
			if index == 'projects':
				doc = Project.get(using=client, index=index, id=id)
			elif index == 'publications':
				doc = Publication.get(using=client, index=index, id=id)

			if doc.element_tags:
				current_tags = list(doc.element_tags)
			else:
				current_tags = []

			current_tags.append(tag)
			current_tags_set = set(current_tags)
			doc.update(using=client,index=index,element_tags=list(current_tags_set))

			print(f'{index} - doc ({id}): updated with {tag}')




from elastic import client
import elasticsearch as es
from elasticsearch_dsl import Q, Search
import json

class Query(object):
	"""
	The Query class construts and returns an Elasticsearch
	query object.


	"""
	def __init__(self, must_match=[], 
		should_match=[], must_not_match=[]):

		self.set_must(must_match)
		self.set_should(should_match)
		self.set_must_not(must_not_match)
		self.construct_query()

	def match(self, query, field, name='match'):
		"""
		Return 'match' query object for the provided
		query and field.

		Parameters
		----------
		query : str
			The provided query string.
		field : str
			The field to be queried.
		[name] : str
			A name given to the query.

		Returns
		-------
		A query object for the provided query and field.

		"""
		# construct the query
		q = Q(
			{
				"match": {
					f"{field}": {
						"query": query,
						"_name": f"{name}:{field}:{query.replace(' ','_')}"
					}
				}
			}
		)

		return q

	def construct_boolean_clause(self, must_queries=[], 
		should_queries=[], must_not_queries=[]):
		"""
		Return 'bool' query object for the provided 'must',
		'should', and 'must_not' queries.

		'must' queries require a document to match the query in
		the provided field for the specified query type.

		'must_not' queries exclude documenta that match the query
		in the provided field for the specified query type.

		'should' queries only affect the relevance score of the
		matched documents (i.e. the ordering of the documents returned).

		Parameters
		----------
		must : list [(field,query),...]
		should : list [(field,query),...]
		must_not : list [(field,query),...]

		Returns
		-------
		A query object for the provided queries and field(s).

		"""

		def get_queries(field_query_list):
			# example input: queries=[(field,query),...]
			queries = []
			for field, query in field_query_list:
				queries.append(self.match(query, field))
			return queries

		must = []
		should = [] 
		must_not = []

		# must queries
		if must_queries:
			must = get_queries(must_queries)
		# get should queries
		if should_queries:
			should = get_queries(should_queries)
		# get must_not queries
		if must_not_queries:
			must_not = get_queries(must_not_queries)

		# construct the query
		return Q("bool", must=must, should=should, must_not=must_not)

	def set_must(self, field_query_list):
		must = []
		if field_query_list:
			must = self.construct_boolean_clause(should_queries=field_query_list)
		self.must = must

	def set_should(self, field_query_list):
		should = []
		if field_query_list:
			should = self.construct_boolean_clause(should_queries=field_query_list)
		self.should = should

	def set_must_not(self, field_query_list):
		must_not = []
		if field_query_list:
			must_not = self.construct_boolean_clause(should_queries=field_query_list)
		self.must_not = must_not

	def construct_query(self):
		q = Q("bool", must=self.must, should=self.should, must_not=self.must_not)
		self.query = q

	def to_dict(self):
		return self.query.to_dict()

	def __str__(self):
		return json.dumps(self.to_dict(), indent=2)


def get_query_fields(query):

	fields = ["title","abstract"]
	all_ngrams = ["bigram", "trigram", "quadragram", "pentagram"]

	n_terms = len(query.split())
	if n_terms > 1:
		ngrams = all_ngrams[:n_terms-1]
		fields = [".".join([field, ngram]) for field in fields for ngram in ngrams]
	
	return fields


def get_query_terms(query):

	# topics

	construction_quality = dict(
		must_match=["construction"],
		should_match=["quality", "construction quality"]
	)

	design_and_details = dict(
		must_match=["design"],
	)

	material_specifications = dict(
		must_match=["materials"],
		should_match=["material specifications"]
	)

	live_load = dict(
		must_match=["live load"]
	)

	environment = dict(
		must_match=["environment"]
	)

	maintenance_and_preservation = dict(
		must_match=["maintenance", "preservation"],
		should_match=["maintenance and preservation"]
	)

	structural_integrity = dict(
		must_match=["structural integrity"]
	)

	structural_condition = dict(
		must_match=["condition"],
		should_match=["structural condition"]
	)

	functionality = dict(
		must_match=["functionality"]
	)

	cost = dict(
		must_match=["cost"]
	)

	# Elements

	bridges = dict(
		must_match=["bridge"]
	)

	untreated_deck = dict(
		must_match=["decks"],
		must_not_match=["overlay", "wearing surface"]
	)

	treated_deck = dict(
		must_match=["overlay", "wearing surface"]
	)

	joints = dict(
		must_match=["joints"]
	)

	bearings = dict(
		must_match=["bearings"]
	)

	coatings = dict(
		must_match=["coating"],
		should_match=["steel coating"]
	)

	prestressing = dict(
		must_match=["prestress", "pre-stress"],
		should_match=["strands"]
	)


	query_terms = dict(
		construction_quality=construction_quality,
		design_and_details=design_and_details,
		material_specifications=material_specifications,
		live_load=live_load,
		environment=environment,
		maintenance_and_preservation=maintenance_and_preservation,
		structural_integrity=structural_integrity,
		structural_condition=structural_condition,
		functionality=functionality,
		cost=cost,
		bridges=bridges,
		untreated_deck=untreated_deck,
		treated_deck=treated_deck,
		joints=joints,
		bearings=bearings,
		coatings=coatings,
		prestressing=prestressing
	)

	return query_terms.get(query)


def apply_filters(s, filters):

	status = filters.get("status")
	if status and status != "all":
		s = s.filter("term", status=status)

	start_date = filters.get('start_date')
	if start_date:
		s = s.filter("range", **{"start_date":{"gte":start_date}})

	publication_date = filters.get('publication_date')
	if publication_date:
		s = s.filter("range", **{"publication_date":{"gte":publication_date}})

	topic = filters.get('topic')
	if topic:
		s = s.filter("term", tags=topic)

	element = filters.get('element')
	if element and element != "all":
		s = s.filter("term", tags=element)

	return s


def get_query_arguments(query):

	query_terms = get_query_terms(query)
	args = dict()
	for key in query_terms:
		args[key] = [(field, term) 
			for term in query_terms.get(key) 
			for field in get_query_fields(term)]
	
	return args


def run_query(q, index, filters=None):
	
	s = Search(
		using=client, 
		index=index
		)
		
	if filters:
		s = apply_filters(s, filters)
	s = s.query(q)

	return s


def process_search_response(s, first=0, last=10):
	""" function that process response from elasticsearch and formats
	the response for front end """
	# process documents returned by the search
	hits = {}
	response = []
	for h in s[first:last]:
		# get data from document fields
		doc_id = h.meta.id
		title = h.title
		abstract = h.abstract
		matched_queries = list(h.meta.matched_queries)
		score = h.meta.score
		trid_terms = [term for term in h.TRID_INDEX_TERMS]
		trid_subjects = [subject for subject in h.TRID_SUBJECT_AREAS]
		
		# store documents returned by the search
		hits[doc_id] = dict(
			id =  doc_id,
			title = title,
			abstract = abstract,
			trid_terms = trid_terms,
			trid_subjects = trid_subjects,
			matched_queries = matched_queries,
			score = score,
			# start_date = start_date,
			# completion_date = actual_completion_date,
			# funding=funding,
			# funding_agencies=funding_agencies,
			# performing_agencies=performing_agencies,
			# managing_agencies=managing_agencies
			# topic_tags = topic_tags,
			# element_tags=element_tags
		)
		response.append(hits[doc_id])
	return hits, response


# filters = dict(
# 	status='all'
# )
# kwargs = get_query_arguments("structural_condition")
# q = Query(**kwargs)
# print(q)
# s = run_query(q.query, index="publications")
# print(s.count())
# hits, response = process_search_response(s, last=s.count())
# print()
# print(json.dumps(response[:5], indent=2))







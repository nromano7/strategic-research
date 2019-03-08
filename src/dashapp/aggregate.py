from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, A, Q
from elastic import query, client

index = 'projects'


def project_count_by_state(queries=None):

	# search object
	s = Search(using=client,index=index)

	if queries:

		tag = queries.get("tag")
		element_tag = queries.get("element_tag")
		filters = dict(
			topic = tag,
			element = element_tag
		)

		s = query.run_query(Q({"match_all":{}}), index=index, filters=filters)

	# aggregations
	a1 = A(
		"nested", 
		path="funding_agencies"
	)
	a2 = A(
		"terms", 
		field="funding_agencies.state.keyword",
		size=50, 
		order={"_count": "desc"}
	)
	a3 = A(
		"terms",
		field="_id",
		size=5000, 
	)

	# chain aggregations and execute
	s.aggs\
		.bucket('agencies', a1)\
		.bucket('states',a2)\
		.bucket('doc_ids', a3)
	response = s.execute()

	# filter response
	res = {}
	for b in response.aggregations.agencies.states.buckets:
		state = b['key']
		doc_count = b['doc_count']
		res[state] = dict(
			doc_count=doc_count,
			doc_ids=[doc['key'] for doc in b.doc_ids.buckets]
		)
	
	return res

def project_count(queries=None):

	# search object
	s = Search(using=client,index=index)

	allStatus = ['Active', 'Completed', 'Programmed', 'Proposed']

	if queries:

		tag = queries.get("tag")
		element_tag = queries.get("element_tag")
		filters = dict(
			element = element_tag,
			topic = tag
		)

		# run query
		# if tag == 'all':
		# 	s = query.run_query(Q({"match_all":{}}), index=index, filters=filters)
		# else:
		# 	kwargs = query.get_query_arguments(tag)
		# 	q = query.Query(**kwargs)
		# 	s = query.run_query(q.query, index='projects', filters=filters)
		s = query.run_query(Q({"match_all":{}}), index=index, filters=filters)
		res={}
		res['total'] = s.count()
		for status in allStatus:
			res[status.lower()] = s.filter("match",status=status).count()

	else:

		# query
		total = Q(
			{
				"match_phrase": {
					"doc_type": {
						"query": "project"
					}
				}
			}
		)
		s=s.query(total)
		res={}
		res['total'] = s.count()
		for status in allStatus:
			q = Q(
				{
					"match_phrase": {
						"status.keyword": {
							"query": status
						}
					}
				}
			)
			res[status.lower()] = s.query(q).count()

	return res

def project_count_by_topic(**kwargs):

	topic_query = kwargs.get("topic")
	topic_filter = kwargs.get("topic_selection")
	element_filter = kwargs.get("element")
	filters = dict(
		element = element_filter,
		topic = topic_filter
	)

	# run query
	kwargs = query.get_query_arguments(topic_query)
	q = query.Query(**kwargs)
	s = query.run_query(q.query, index=index, filters=filters)
	count = s.count()

	# aggregate doc ids
	a1 = A(
		"terms",
		field="_id",
		size=5000, 
	)

	# chain aggregations and execute
	s.aggs.bucket('doc_ids', a1)
	response = s.execute()

	# filter response
	doc_ids = []
	for b in response.aggregations.doc_ids.buckets:
		doc_ids.append(b['key'])

	return count, doc_ids

def publication_count(queries=None):

	 # search object
	s = Search(using=client,index='publications')
	
	if queries:

		tag = queries.get("tag")
		element_tag = queries.get("element_tag")
		filters = dict(
			topic = tag,
			element = element_tag
		)

		index = 'publications'
		# kwargs = query.get_query_arguments(tag)
		# q = query.Query(**kwargs)
		s = query.run_query(Q({"match_all":{}}), index=index, filters=filters)


		count = s.count()

	else:

		# query
		total = Q(
			{
				"match_phrase": {
					"doc_type": {
						"query": "publication"
					}
				}
			}
		)

		count = s.query(total).count()

	return count
	
def funding_by_state(**kwargs):

	# topic_query = kwargs.get("topic")
	topic = kwargs.get("topic")
	element = kwargs.get("element")
	filters = dict(
		element = element,
		topic = topic
	)

	# run query
	s = query.run_query(Q({"match_all":{}}), index=index, filters=filters)

	# aggregations
	a1 = A(
		"nested", 
		path="funding_agencies"
	)
	a2 = A(
		"terms", 
		field="funding_agencies.state.keyword",
		size=50, 
		order={"_count":"desc"},
	)
	a3 = A("reverse_nested")
	a4 = A(
		"range", 
		field="funding", 
		ranges=[
			{
				"from": 0, "to": 100000
			},
			{
				"from": 100000,"to": 250000
			},
			{
				"from": 250000,"to": 500000
			},
			{
				"from": 500000,"to": 750000
			},
			{
				"from": 750000,"to": 1000000
			},
			{
				"from": 1000000
			}
		],
		keyed=True
	)

	# chain aggregations and execute
	s.aggs\
		.bucket('agencies', a1)\
		.bucket('states',a2)\
		.bucket('reverse',a3)\
		.bucket('fund_amt',a4)
	response = s.execute()

	# filter response
	res = {}
	for b in response.aggregations.agencies.states.buckets:
		state = b.key
		if len(state) > 2:
			continue
		if state in res: 
			continue
		buckets = b.reverse.fund_amt.buckets.to_dict()
		res[state] = buckets
	
	return res


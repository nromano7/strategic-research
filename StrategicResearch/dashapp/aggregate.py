from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, A, Q
from elastic import query, client

# AWS_EP = "https://search-strategic-research-67yfnme5nbl3c45vigirwnko4q.us-east-2.es.amazonaws.com/"
# client = Elasticsearch(AWS_EP)
index = 'projects'


def project_count_by_state(queries=None):

	# search object
	s = Search(using=client,index=index)

	if queries:

		tag = queries.get("tag")
		element_tag = queries.get("element_tag")

		q = query.get_topic_query(tag, {"record_set": element_tag}, index)
		s = query.run_query(index, q)

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

	# chain aggregations and execute
	s.aggs\
		.bucket('agencies', a1)\
		.bucket('states',a2)
	response = s.execute()

	# filter response
	res = {}
	for b in response.aggregations.agencies.states.buckets:
		state = b['key']
		doc_count = b['doc_count']
		res[state] = doc_count
	
	return res

def project_count(queries=None):

	# search object
	s = Search(using=client,index=index)

	allStatus = ['Active', 'Completed', 'Programmed', 'Proposed']

	if queries:

		tag = queries.get("tag")
		element_tag = queries.get("element_tag")

		q = query.get_topic_query(tag, {"record_set": element_tag}, index)
		s = query.run_query(index, q)

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
	q = query.get_topic_query(topic_query, filters, index)
	s = query.run_query(index, q)
	count = s.count()

	return count

def publication_count(queries=None):

	 # search object
	s = Search(using=client,index='publications')
	
	if queries:

		tag = queries.get("tag")
		element_tag = queries.get("element_tag")

		index = 'publications'
		q = query.get_topic_query(tag, {"record_set": element_tag}, index)
		s = query.run_query(index, q)

		# if query == "all":
		# 	q=Q({"match_all":{}})
		# else:
		# 	q=Q({"match":{"tags":query}})

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

	topic_query = kwargs.get("topic")
	topic_filter = kwargs.get("topic_selection")
	element_filter = kwargs.get("element")
	filters = dict(
		element = element_filter,
		# topic = topic_filter
	)

	# run query
	q = query.get_topic_query(topic_query, filters, index)
	s = query.run_query(index, q)

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

# topic_selection = "construction_quality"
# element_selection = "untreated_deck"
# data =funding_by_state(topic=topic_selection, element=element_selection)

# print()

# def funding_by_state(query=None):

# 	# search object
# 	s = Search(using=client,index=index)

# 	if query:

# 		# fields to query
# 		fields = ["title","abstract","notes","TRID_INDEX_TERMS","TRID_SUBJECT_AREAS",'tags']
		
# 		q=Q(
# 			{
# 				"multi_match":{
# 					"query": query,
# 					"type":"best_fields",
# 					"fields":fields
# 				}
# 			}
# 		)
# 		s=s.query(q)

# 	# aggregations
# 	a1 = A(
# 		"nested", 
# 		path="funding_agencies"
# 	)
# 	a2 = A(
# 		"terms", 
# 		field="funding_agencies.state.keyword",
# 		size=50, 
# 		order={"_count":"desc"},
# 	)
# 	a3 = A("reverse_nested")
# 	a4 = A(
# 		"range", 
# 		field="funding", 
# 		ranges=[
# 			{
# 				"from": 0, "to": 100000
# 			},
# 			{
# 				"from": 100000,"to": 250000
# 			},
# 			{
# 				"from": 250000,"to": 500000
# 			},
# 			{
# 				"from": 500000,"to": 750000
# 			},
# 			{
# 				"from": 750000,"to": 1000000
# 			},
# 			{
# 				"from": 1000000
# 			}
# 		],
# 		keyed=True
# 	)

# 	# chain aggregations and execute
# 	s.aggs\
# 		.bucket('agencies', a1)\
# 		.bucket('states',a2)\
# 		.bucket('reverse',a3)\
# 		.bucket('fund_amt',a4)
# 	response = s.execute()

# 	# filter response
# 	res = {}
# 	for b in response.aggregations.agencies.states.buckets:
# 		state = b.key
# 		buckets = b.reverse.fund_amt.buckets.to_dict()
# 		res[state] = buckets
	
# 	return res

# topic_selection = "all"
# element_selection = "all"

# attributes=['live_load', 'environment', 'maintenance_and_preservation',]
# counts=[project_count_by_topic(topic=attr, element=element_selection, topic_selection=topic_selection) for attr in attributes]

# print()
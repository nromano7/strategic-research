# from StrategicResearch import TOPIC_TAGS, ELEMENT_TAGS
from flask import render_template, request, session, url_for
from flaskapp import application
from elastic import query
from elasticsearch_dsl import Q
from dashapp.dashapp import app as dashapp
import json

topics = [
	'construction_quality','design_and_details','material_specifications',
	'live_load', 'environment', 'maintenance_and_preservation',
	'structural_integrity', 'structural_condition', 'functionality', 'cost'
]
formatted_topic={t:t.title().replace("_"," ").replace("And","&") for t in topics}

@application.route("/")
@application.route("/analyze")
def analyze():
	# return "Analysis"
	return render_template('analyze.html', 
							title='Dashboard', 
							heading='Analyze')


@application.route("/explore", methods=['GET', 'POST'])
def explore():

	# get and handle form data
	# TODO: screen form inputs
	doc_type = request.form.get('recordType','project')
	sort_by = request.form.get('sortBy','sortBy_score')

	filters=dict(
		element = request.form.get('element','superstructure'),
		status = request.form.get('status','all'),
		date_range = request.form.get('dateRange','5'),
		sort_by=sort_by,
		doc_type=doc_type
	)

	TOPIC_TAGS = [
		'construction_quality','design_and_details','material_specifications',
		'live_load', 'environment', 'maintenance_and_preservation',
		'structural_integrity', 'structural_condition', 'functionality', 'cost'
	]

	content = dict()
	for topic in TOPIC_TAGS:

		# specify index
		if doc_type == 'project':
			index = 'projects'
		elif doc_type == 'publication':
			index = 'publications'

		# run query and process response
		kwargs = query.get_query_arguments(topic)
		q = query.Query(**kwargs)
		s = query.run_query(q.query, index=index, filters=filters)
		# _, response = query.process_search_response(s, last=s.count())
		
		# if topic == 'construction_quality':
		# 	content[topic] = response
		# else:
		s = s[:100] # pagination
		r = s.execute()
		content[topic] = r

	return render_template('explore.html', 
							content=content, 
							buttonStates=filters, 
							heading='Explore')


@application.route("/analyze/results", methods=['GET'])
def results():
	# return "Analysis"

	# hande get requests
	all_ = request.args.get('all')
	search = request.args.get('search')
	cat = request.args.get('cat')
	selected_state = request.args.get('state')
	selected_funding = request.args.get('fund')
	filter_topic = request.args.get('topic')
	filter_element = request.args.get('element')


	# handle post requests
	doc_type = request.form.get('recordType','project')
	# sort_by = request.form.get('sortBy','sortBy_score')
	# filters=dict(
	# 	topic = filter_topic,
	# 	element = request.form.get('element','superstructure'),
	# 	status = request.form.get('status','all'),
	# 	date_range = request.form.get('dateRange','5'),
	# 	sort_by=sort_by,
	# 	doc_type=doc_type
	# )

	# specify index
	if doc_type == 'project':
		index = 'projects'
	elif doc_type == 'publication':
		index = 'publications'

	# handle queries
	if all_: # if user clicked project count in dashboard
		clicked = f"{formatted_topic[filter_topic]}"
		if all_ == 'PRJ':
			index = 'projects'
			doc_type = 'project'
		elif all_ == 'PUB':
			index = 'publications'
			doc_type = 'publication'
		filters = dict(
			topic=filter_topic,
			element=filter_element,
			doc_type=doc_type,
			date_range='50'
		)
		kwargs = query.get_query_arguments(filter_topic)
		q = query.Query(**kwargs)
		s = query.run_query(q.query, index=index, filters=filters)

	elif selected_state and selected_funding: # if user clicked cell in heat map
		clicked = f"{selected_state} {selected_funding}"

	elif selected_state: # if user clicked state on map
		clicked = f"{selected_state}"
		filters = dict(
			topic=filter_topic,
			element=filter_element,
			doc_type=doc_type,
			status = request.form.get('status','all'),
			date_range = request.form.get('dateRange','50')
		)
		q = Q({"nested" : {
					"path" : "funding_agencies",
					"query" : {
						"bool" : {
							"must" : [
								{ "match" : {"funding_agencies.state" : selected_state} }
							]
						}
					}
				}
				
			}
		)
			
		s = query.run_query(q, index=index, filters=filters)
		

	elif cat: # if user clicked on bar chart
		clicked = formatted_topic[cat]
		filters = dict(
			topic=filter_topic,
			element=filter_element,
			doc_type=doc_type,
			status = request.form.get('status','all'),
			date_range = request.form.get('dateRange','50')
		)
		kwargs = query.get_query_arguments(cat)
		q = query.Query(**kwargs)
		s = query.run_query(q.query, index=index, filters=filters)

	elif search: # if a free search was requested by the user
		clicked = search
		match_args = query.get_query_arguments(search)
		q = query.Query(must_match=match_args)
		s = query.run_query(q.query, index=index, filters=None)
		filters = dict(
			doc_type=doc_type,
			status = request.form.get('status','all'),
			date_range = request.form.get('dateRange','50')
		)
	
		

	s = s[:1000] # pagination
	r = s.execute()
	
	
	return render_template('results.html', 
							title='Results', 
							heading=f'Search Results',
							content=r, 
							clicked=clicked,
							filters=filters,
							buttonStates=filters)

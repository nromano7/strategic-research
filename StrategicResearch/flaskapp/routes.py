# from StrategicResearch import TOPIC_TAGS, ELEMENT_TAGS
from flask import render_template, request, session, url_for
from flaskapp import application
from elastic import client, models, query
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
		s = s[:500] # pagination
		r = s.execute()
		content[topic] = r

	return render_template('explore.html', 
							content=content, 
							buttonStates=filters, 
							heading='Explore')


@application.route("/search", methods=['GET', 'POST'])
def results():

	# format for front end display
	formatstr = lambda s: s.replace("_"," ")

	if request.method == 'GET':
		# retrieve get requests
		search_type = request.args.get('type','search')
		search_query = request.args.get('query')
		index = request.args.get('index','projects')
		filter_topic = request.args.get('topic','all')
		filter_element = request.args.get('element','all')
		filter_status = request.args.get('status','all')
		date_range = request.args.get('dateRange','50')
		sort_by = request.args.get('sortBy','date')
		doc_type = index[:-1]

	if request.method == 'POST' and request.form['form'] == 'filters':
	# update record based on form submission
		search_type = request.form.get('type','search')
		search_query = request.form.get('query')
		index = request.form.get('index','projects')
		filter_topic = request.form.get('topic','all')
		filter_element = request.form.get('element','all')
		filter_status = request.form.get('status','all')
		date_range = request.form.get('dateRange','50')
		sort_by = request.form.get('sortBy','date')
		doc_type = index[:-1]

	if request.method == 'POST' and request.form['form'] == 'record':
	# update record based on form submission
		search_type = request.form.get('type','search')
		search_query = request.form.get('query')
		index = request.form.get('index','projects')
		filter_topic = request.form.get('topic','all')
		filter_element = request.form.get('element','all')
		filter_status = request.form.get('status','all')
		date_range = request.form.get('dateRange','50')
		sort_by = request.form.get('sortBy','date')
		doc_type = index[:-1]

		objectives = []
		notes= None
		for key in request.form:
			if key in {'index','doc_id'}:
				continue
			if 'objective' in key:
			# store objectives 
				objectives.append(key)
			if 'notes' in key and request.form.get(key):
			# store notes 
				notes = request.form.get(key)
				# notes = notes.strip()
		
		index = request.form.get('index')
		doc_id = request.form.get('doc_id')
		print(doc_id)
		# update objectives and notes field for doc in database
		client.update(index=index, doc_type='doc', id=doc_id,
                body={"doc": {"objectives": objectives, "notes": notes }})
	
	

	# handle requests
	if search_type == 'click_count': 
	# if user clicked project or pub count in dashboard

		if filter_topic != 'all' and filter_element != 'all': 
		# user filtered topic and elements in dashboard
			clicked = f'for "{formatstr(filter_topic)}" and "{formatstr(filter_element)}"'
		elif filter_topic != 'all' and filter_element =='all':
		# user filtered topic in dashboard
			clicked = f'for "{formatstr(filter_topic)}"'
		elif filter_topic == 'all' and filter_element != 'all':
		# user filtered element in dashboard
			clicked = f'for "{formatstr(filter_element)}"'
		elif filter_topic == 'all' and filter_element == 'all':
		# no filters
			clicked = f"for all topics and elements"

		filters = dict(
			topic=filter_topic,
			element=filter_element,
			doc_type=doc_type,
			date_range=date_range,
			sort_by=sort_by
		)

		q = Q({"match_all": {}}) # note: sorting does not apply to match all
		s = query.run_query(q, index=index, filters=filters)

	elif search_type == 'click_bar': 
	# if user clicked on bar chart

		if search_query == filter_topic and filter_element != 'all': 
		# user filtered topic and elements in dashboard
			clicked = f'for "{formatstr(search_query)}" and "{formatstr(filter_element)}"'
		elif search_query == filter_topic and filter_element =='all':
		# user filtered topic in dashboard
			clicked = f'for "{formatstr(search_query)}"'
		elif search_query != filter_topic and filter_topic != 'all' and filter_element != 'all':
		# user filtered topic and elements in dashboard, and clicked on different bar
			clicked = f'for "{formatstr(search_query)}", "{formatstr(filter_topic)}", and "{formatstr(filter_element)}"'
		elif search_query != filter_topic and filter_topic != 'all' and  filter_element == 'all':
		# user filtered topic in dashboard, and clicked on different bar
			clicked = f'for "{formatstr(search_query)}", and "{formatstr(filter_topic)}"'
		elif search_query != filter_topic and filter_topic == 'all' and  filter_element != 'all':
		# user filtered elements in dashboard, and clicked on different bar
			clicked = f'for "{formatstr(search_query)}", and "{formatstr(filter_element)}"'
		else:
		# no filters
			clicked = f'for "{formatstr(search_query)}", all topics and elements'

		filters = dict(
			topic = filter_topic,
			element = filter_element,
			doc_type = doc_type,
			status = filter_status,
			date_range = date_range,
			sort_by = sort_by
		)

		kwargs = query.get_query_arguments(search_query)
		q = query.Query(**kwargs)
		s = query.run_query(q.query, index=index, filters=filters)

	elif search_type == 'click_map': 
	# if user clicked state on map

		if filter_topic != 'all' and filter_element != 'all': 
		# user filtered topic and elements in dashboard
			clicked = f'for "{search_query}", "{formatstr(filter_topic)}", and "{formatstr(filter_element)}"'
		elif filter_topic != 'all' and filter_element =='all':
		# user filtered topic in dashboard
			clicked = f'for "{search_query}", and "{formatstr(filter_topic)}"'
		elif filter_topic == 'all' and filter_element != 'all':
		# user filtered element in dashboard
			clicked = f'for "{search_query}", and "{formatstr(filter_element)}"'
		elif filter_topic == 'all' and filter_element == 'all':
		# no filters
			clicked = f'for "{search_query}", all topics and elements'

		filters = dict(
			topic=filter_topic,
			element=filter_element,
			doc_type=doc_type,
			status = filter_status,
			date_range = date_range,
			sort_by=sort_by
		)

		q = Q({"nested" : {
					"path" : "funding_agencies",
					"query" : {
						"bool" : {
							"must" : [
								{ "match" : {"funding_agencies.state" : search_query} }
							]
						}
					}
				}
				
			}
		)
			
		s = query.run_query(q, index=index, filters=filters)

	elif search_type == 'search': 
	# if a free search was requested by the user

		if filter_topic != 'all' and filter_element != 'all': 
		# user filtered topic and elements in dashboard
			clicked = f'for "{search_query}", "{formatstr(filter_topic)}" and "{formatstr(filter_element)}"'
		elif filter_topic != 'all' and filter_element =='all':
		# user filtered topic in dashboard
			clicked = f'for "{search_query}", and "{formatstr(filter_topic)}"'
		elif filter_topic == 'all' and filter_element != 'all':
		# user filtered element in dashboard
			clicked = f'for "{search_query}", and "{formatstr(filter_element)}"'
		elif filter_topic == 'all' and filter_element == 'all':
		# no filters
			clicked = f'for "{search_query}", all topics and elements'

		filters = dict(
			topic=filter_topic,
			element=filter_element,
			doc_type=doc_type,
			status = filter_status,
			date_range = date_range,
			sort_by='both'
		)
		q = Q({"multi_match" : {
			"query" : search_query,
			"fields" : [ "title", "abstract" ] 
			}
		})
		s = query.run_query(q, index=index, filters=filters)

	s = s[:1000] # pagination
	r = s.execute()
	
	buttonStates=dict(
		topic = filter_topic,
		element = filter_element,
		status = filter_status,
		date_range = date_range,
		sort_by = sort_by,
		doc_type = doc_type
	)

	formdata = dict(
		type=search_type,
		query=search_query,
		index=index,
		topic=filter_topic,
		element=filter_element,
		status=filter_status,
		date_range=date_range,
		sort_by=sort_by
	) 
	
	return render_template('results.html', 
							title='Results', 
							heading=f'Search Results',
							content=r, 
							clicked=clicked,
							buttonStates=buttonStates,
							formdata=formdata)


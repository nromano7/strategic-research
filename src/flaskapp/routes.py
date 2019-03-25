import datetime
from flask import render_template, request, session, url_for, redirect
from flaskapp import application
from elastic import client, models, query, index#, PROJECT_FILES_PATH, PUB_FILES_PATH
from elasticsearch_dsl import Q
from dashapp.dashapp import app as dashapp
import json
from webscrapper import trid_get as webscrapper
import shutil
import os

topics = [
	'construction_quality','design_and_details','material_specifications',
	'live_load', 'environment', 'maintenance_and_preservation',
	'structural_integrity', 'structural_condition', 'functionality', 'cost'
]
formatted_topic={t:t.title().replace("_"," ").replace("And","&") for t in topics}

element_tags = [
	'superstructure', 'untreated_deck', 'treated_deck', 'joints', 
	'bearings', 'coatings', 'prestressing'
]

@application.route("/")
@application.route("/analyze")
def analyze():
	# return "Analysis"
	last_update = client.get(index='appdata', doc_type='doc', id=1)['_source']['last_update']
	content = dict(
		bookmarked=query.run_query(Q("term",bookmarked=True), index=['projects','publications'])[:1000].execute(),
		obj1=query.run_query(Q("term",objectives="objective1"), index=['projects','publications'])[:1000].execute(),
		obj2=query.run_query(Q("term",objectives="objective2"), index=['projects','publications'])[:1000].execute(),
		obj3=query.run_query(Q("term",objectives="objective3"), index=['projects','publications'])[:1000].execute(),
		obj4=query.run_query(Q("term",objectives="objective4"), index=['projects','publications'])[:1000].execute(),
	)
	formdata = dict(
		type=-1,
		query=-1,
		index=-1,
		topic=-1,
		element=-1,
		status=-1,
		date_range=-1,
		sort_by=-1
	) 
	return render_template('analyze.html', 
							title='Dashboard', 
							heading='Analyze',
							last_update=last_update,
							content=content,
							formdata=formdata)


@application.route("/explore", methods=['GET', 'POST'])
def explore():

	# get and handle form data
	search_type = request.form.get('type','search')
	search_query = request.form.get('query')
	index = request.form.get('index','projects')
	filter_topic = request.form.get('topic','all')
	filter_element = request.form.get('element','all')
	filter_status = request.form.get('status','all')
	date_range = request.form.get('dateRange','50')
	sort_by = request.form.get('sortBy','date')
	doc_type = index[:-1]

	filters=dict(
		element = filter_element,
		status = filter_status,
		date_range = date_range,
		sort_by = sort_by,
		doc_type = doc_type
	)

	content = dict()
	for topic in topics:

		# run query and process response
		kwargs = query.get_query_arguments(topic)
		q = query.Query(**kwargs)
		s = query.run_query(q.query, index=index, filters=filters)
		s = s[:100] # pagination
		r = s.execute()
		content[topic] = r

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

	buttonStates=dict(
		topic="None",
		element = filter_element,
		status = filter_status,
		date_range = date_range,
		sort_by = sort_by,
		doc_type = doc_type
	)

	last_update = client.get(index='appdata', doc_type='doc', id=1)['_source']['last_update']
	return render_template('explore.html', 
							content=content, 
							buttonStates=buttonStates, 
							formdata=formdata,
							heading='Explore',
							last_update=last_update)


@application.route("/search", methods=['GET', 'POST'])
def results():

	if request.referrer.split('/')[-1] == 'update':
		return redirect(url_for('results'))

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
	# retrieve form submission
		search_type = request.form.get('type','search')
		search_query = request.form.get('query')
		index = request.form.get('index','projects')
		filter_topic = request.form.get('topic','all')
		filter_element = request.form.get('element','all')
		filter_status = request.form.get('status','all')
		date_range = request.form.get('dateRange','50')
		sort_by = request.form.get('sortBy','date')
		doc_type = index[:-1]
	

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
			clicked = f"for all {index}"

		filters = dict(
			topic=filter_topic,
			element=filter_element,
			doc_type=doc_type,
			date_range=date_range,
			status = filter_status,
			sort_by=sort_by
		)
		if filter_topic == 'all':
			if filter_element == 'all':
				q = Q({"match_all": {}}) # note: sorting does not apply to match all
				s = query.run_query(q, index=index, filters=filters)
			else:
				kwargs = query.get_query_arguments(filter_element)
				q = query.Query(**kwargs)
				s = query.run_query(q.query, index=index, filters=filters)
		else:
			kwargs = query.get_query_arguments(filter_topic)
			q = query.Query(**kwargs)
			s = query.run_query(q.query, index=index, filters=filters)
		

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
			clicked = f'for "{formatstr(search_query)}"'

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
			clicked = f'for "{search_query}"'

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

	elif search_type == 'search' and search_query != 'None': 
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
			clicked = f'for "{search_query}"'

		filters = dict(
			topic=filter_topic,
			element=filter_element,
			doc_type=doc_type,
			status = filter_status,
			date_range = date_range,
			sort_by=sort_by
		)
		
		q = Q({"multi_match" : {
			"query" : search_query,
			"fields" : [ "title", "abstract" ] 
			}
		})

		s = query.run_query(q, index=index, filters=filters)

	else:
		if request.referrer.split('/')[-1] == 'explore':
			return redirect(url_for('explore'))


	s = s[:1000] # pagination
	r = s.execute()
	# print(r[0].objectives)
	
	buttonStates=dict(
		type = search_type,
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
	
	last_update = client.get(index='appdata', doc_type='doc', id=1)['_source']['last_update']
	return render_template('results.html', 
							title='Results', 
							heading=f'Search Results',
							content=r, 
							clicked=clicked,
							buttonStates=buttonStates,
							formdata=formdata,
							last_update=last_update)


@application.route("/update/record/annotate", methods=['GET', 'POST'])
def annotate():

	if request.method == 'POST':
	# update record from form submission
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
		
		doc_id = request.form.get('doc_id')
		# update objectives and notes field for doc in database
		client.update(index=index, doc_type='doc', id=doc_id,
                body={"doc": {"objectives": objectives, "notes": notes }})

		args = dict(
			type = search_type,
			query = search_query,
			index = index,
			topic = filter_topic,
			element = filter_element,
			status = filter_status,
			dateRange = date_range,
			sortBy = sort_by
		)

	return 'form submitted'


@application.route("/update/record/bookmark", methods=['GET', 'POST'])
def bookmark():
	
	index = request.form.get('index','projects')
	doc_id = request.form.get('doc_id')
	marked = request.form.get('marked')
	# update objectives and notes field for doc in database
	client.update(index=index, 
			doc_type='doc', 
			id=doc_id,
			body={"doc": {"bookmarked":marked}})

	return 'doc updated'


@application.route("/update/database", methods=['GET', 'POST'])
def update_database():

	now = datetime.datetime.now()
	year, month, day = now.year, now.month, now.day

	# create temporary directory for downloading files
	CWD = os.getcwd()
	TMP_DIRECTORY = os.path.join(CWD, r'.tmp')
	DOWNLOADS_FOLDER = os.path.join(TMP_DIRECTORY,f"{year:04}{month:02}{day:02}")
	XML_PATH = os.path.join(DOWNLOADS_FOLDER, "xml")
	JSON_PATH = os.path.join(DOWNLOADS_FOLDER, "json")
	PROJECT_FILES_PATH = os.path.join(JSON_PATH,"projects")
	PUB_FILES_PATH = os.path.join(JSON_PATH,"publications")

	try:
		shutil.rmtree(TMP_DIRECTORY)
	except:
		pass

	os.makedirs(DOWNLOADS_FOLDER)
	os.makedirs(XML_PATH)
	os.makedirs(JSON_PATH)
	os.makedirs(PROJECT_FILES_PATH)
	os.makedirs(PUB_FILES_PATH)

	# scrape TRID site
	webscrapper.scrape_trid(TMP_DIRECTORY, DOWNLOADS_FOLDER)

	# index documents
	index.index_documents("projects", PROJECT_FILES_PATH)
	index.tag_documents("projects", topics, element_tags)
	index.index_documents("publications", PUB_FILES_PATH)
	index.tag_documents("publications", topics, element_tags)

	# delete temporary downloads directory
	shutil.rmtree(TMP_DIRECTORY)

	# update appData index
	today = str(datetime.date.today())
	client.update(index='appdata', doc_type='doc', id=1, body={'doc':{'last_update':today}})

	return "database updated"
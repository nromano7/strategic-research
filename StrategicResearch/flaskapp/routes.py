# from StrategicResearch import TOPIC_TAGS, ELEMENT_TAGS
from flask import render_template, request, session, url_for
from flaskapp import application
from elastic import query
from dashapp.dashapp import app as dashapp
import json

@application.route("/", methods=['GET', 'POST'])
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

@application.route("/analyze")
def analyze():
	# return "Analysis"
	return render_template('analyze.html', 
							title='Dashboard', 
							heading='Analyze')

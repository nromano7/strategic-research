# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import dashapp.figure as fig
import dashapp.aggregate as aggregate
from datetime import datetime as dt
from flaskapp import application as flaskapp
import textwrap

# external css and js
external_stylesheets = [
	"https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
	"https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0/css/bootstrap.min.css",
	"https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.5.4/css/mdb.min.css",
]
external_scripts = [
	"https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js",
	"https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.13.0/umd/popper.min.js",
	"https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0/js/bootstrap.min.js",
	"https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.5.4/js/mdb.min.js",
	'https://cdn.plot.ly/plotly-1.37.0.min.js'
]

# initialize dash app
app = dash.Dash(__name__, 
	sharing=True,
	server=flaskapp, 
	url_base_pathname='/dashboard/',
	external_scripts=external_scripts,
	external_stylesheets=external_stylesheets
)

""" ------------------------------- LAYOUT --------------------------------- """

app.layout = html.Div(
	className="dash-grid-container grey lighten-3",
	children=[
		html.Div(
			id="filter-panel",
			className="card card-body z-depth-1 pt-2",
			children=[
				# html.H4("Filter Options"),
				html.Div(
					className="row",
					children=[
						html.Div(
							className="col text-left p-2",
							children=[
								html.H6("Filter by research topic."),
								dcc.Dropdown(
									id="tags-selection",
									className="text-left",
									options=[
										dict(label="All Research Topics ", value="all"),
										dict(label="Construction Quality", value="construction_quality"),
										dict(label="Design & Details", value="design_and_details"),
										dict(label="Material Specifications", value="material_specifications"),
										dict(label="Live Load", value="live_load"),
										dict(label="Environment", value="environment"),
										dict(label="Maintenance & Preservation", value="maintenance_and_preservation"),
										dict(label="Structural Integrity", value="structural_integrity"),
										dict(label="Structural Condition", value="structural_condition"),
										dict(label="Functionality", value="functionality"),
										dict(label="Cost", value="cost")
									],
									placeholder="Select research topic...",
									value="all",
									searchable=False,
									clearable=False,
								)
							]
						),
						html.Div(
							className="col text-left p-2",
							children=[
								html.H6("Filter by bridge element."),
								dcc.Dropdown(
									id="record-set-selection",
									className="text-left",
									options=[
										dict(label="All Bridges & Structures", value="all"),
										dict(label="All Superstrcuture", value="superstructure"),
										dict(label="Untreated Decks", value="untreated_deck"),
										dict(label="Treated Decks", value="treated_deck"),
										dict(label="Joints", value="joints"),
										dict(label="Bearings", value="bearings"),
										dict(label="Steel Coatings", value="coatings"),
										dict(label="Prestressing", value="prestressing")
									],
									placeholder="Select bridge element...",
									value="all",
									searchable=False,
									clearable=False
								)
							]
						),
					],
				),
				# html.Div(
				# 	className = "row",
				# 	children = [
				# 		html.Div(
				# 			className="col w-100",
				# 			children=[
				# 				dcc.DatePickerRange(
				# 					id='date-picker-range',
				# 					start_date=dt(2017, 5, 3),
				# 					end_date_placeholder_text='Select a date!'
				# 				),
				# 			]
				# 		)
				# 	]
				# )
			]
		),
		html.Div(
			id="projects-panel",
			className="card card-body text-center justify-content-center z-depth-1 p-1",
			children=[
				html.H2(
					id="project-count",
					children=[
						html.A("{:,d}".format(aggregate.project_count()['total']))
					]
				),
				html.H3("Projects", className="text-muted")
			]
		),
		html.Div(
			id="publications-panel",
			className="card card-body text-center justify-content-center z-depth-1 p-1",
			children=[
				html.H2(
					id="publication-count",
					children=[
						html.A("{:,d}".format(aggregate.publication_count()))
					]
				),
				html.H3("Publications", className="text-muted")
			]
		),
		dcc.Graph(
			id='project-count-map',
			className="z-depth-1",
			figure = fig.project_count_map(),
			config={'displayModeBar': False}
		),
		html.H4("Count by State",id="project-count-map-heading",className="p-2 text-left"),
		dcc.Graph(
			id='funding-heatmap',
			className="z-depth-1",
			config={'displayModeBar': False}
		),
		html.H4("Funding by State",id="funding-heatmap-heading",className="p-2 text-left"),
		dcc.Graph(
			id='barchart1',
			className="z-depth-1",
			config={'displayModeBar': False}
		),
		html.Div(
			id="barchart1-heading",
			children=[
				html.H4("Bridge Attributes",className="pl-2 pt-2 m-0 text-left"),
				html.H6("(Total Records)",className="pl-2 text-left")
			]
		),
		dcc.Graph(
			id='barchart2',
			className="z-depth-1",
			config={'displayModeBar': False}
		),
		html.Div(
			id="barchart2-heading",
			children=[
				html.H4("Inputs",className="pl-2 pt-2 m-0 text-left"),
				html.H6("(Total Records)",className="pl-2 text-left")
			]
		),
		dcc.Graph(
			id='barchart3',
			className="z-depth-1",
			config={'displayModeBar': False}
		),
		html.Div(
			id="barchart3-heading",
			children=[
				html.H4("Bridge Performance",className="pl-2 pt-2 m-0 text-left"),
				html.H6("(Total Records)",className="pl-2 text-left")
			]
		)
	]
)

""" ----------------------------- CALLBACKS ------------------------------- """


""" callback function for updating the project count """
@app.callback(dash.dependencies.Output('project-count','children'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])
def callback_project_count(tag, element_tag):
	print(tag)
	queries = dict(tag=tag, element_tag=element_tag)
	children=[
		html.A(
			href=f"/analyze/results?all=PRJ&cat={tag}&topic={tag}&element={element_tag}",
			target="_blank",
			children=[
				"{:,d}".format(aggregate.project_count(queries=queries)['total'])
			]
		)
	]
	return children


""" callback function for updating the publication count """
@app.callback(dash.dependencies.Output('publication-count','children'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])
def callback_publication_count(tag, element_tag):
	queries = dict(tag=tag, element_tag=element_tag)
	children=[
		html.A(
			href=f"/analyze/results?all=PUB&cat={tag}&topic={tag}&element={element_tag}",
			target="_blank",
			children=[
				"{:,d}".format(aggregate.publication_count(queries=queries))
			]
		)
	]
	return children


""" callback function for updating the project count map """
@app.callback(dash.dependencies.Output('project-count-map','figure'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])
def callback_project_count_map(tag, element_tag):
	queries = dict(tag=tag, element_tag=element_tag)
	data = aggregate.project_count_by_state(queries=queries)
	params = f"topic={tag}&element={element_tag}"
	figure = fig.project_count_map(data=data, params=params)
	return figure


""" callback function for updating attribute bar chart """
@app.callback(dash.dependencies.Output('barchart1','figure'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])
def callback_attribute_barchart(topic_selection, element_selection):
	# format bar labels
	attributes=['construction_quality','design_and_details','material_specifications']
	formatted_attributes=[attr.title().replace("_"," ").replace("And","&") for attr in attributes]
	labels=["<br>".join(textwrap.wrap(label, width=15)) for label in formatted_attributes]
	# get project counts and doc_ids
	counts, ids = [], []
	for attr in attributes:
		count, id = aggregate.project_count_by_topic(topic=attr, 
			element=element_selection, 
			topic_selection=topic_selection)
		counts.append(count)
		ids.append(id)
	# get request parameters
	params = [f"cat={attr}&topic={topic_selection}&element={element_selection}" for attr in attributes]
	# generate figure
	figure = fig.bar_chart(labels=labels, counts=counts, ids=ids, params=params)
	return figure


""" callback function for updating inputs bar chart """
@app.callback(dash.dependencies.Output('barchart2','figure'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])
def callback_input_barchart(topic_selection, element_selection):
	# format bar labels
	inputs=['live_load', 'environment', 'maintenance_and_preservation']
	formatted_inputs=[inp.title().replace("_"," ").replace("And","&") for inp in inputs]
	labels=["<br>".join(textwrap.wrap(label, width=15)) for label in formatted_inputs]
	# get project counts and doc_ids
	counts, ids = [], []
	for i in inputs:
		count, id = aggregate.project_count_by_topic(topic=i, 
			element=element_selection, 
			topic_selection=topic_selection)
		counts.append(count)
		ids.append(id)
	# get request parameters
	params = [f"cat={i}&topic={topic_selection}&element={element_selection}" for i in inputs]
	# generate figure
	figure = fig.bar_chart(labels=labels, counts=counts, ids=ids, params=params)
	return figure


""" callback function for updating performance bar chart """
@app.callback(dash.dependencies.Output('barchart3','figure'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])
def callback_performance_barchart(topic_selection, element_selection):
	# format bar labels
	performance=['structural_integrity', 'structural_condition', 'functionality', 'cost']
	formatted_performance=[perf.title().replace("_"," ").replace("And","&") for perf in performance]
	labels=["<br>".join(textwrap.wrap(label, width=15)) for label in formatted_performance]
	# get project counts and doc_ids
	counts, ids = [], []
	for p in performance:
		count, id = aggregate.project_count_by_topic(topic=p, 
			element=element_selection, 
			topic_selection=topic_selection)
		counts.append(count)
		ids.append(id)
	# get request parameters
	params = [f"cat={perf}&topic={topic_selection}&element={element_selection}" for perf in performance]
	# generate figure
	figure = fig.bar_chart(labels=labels, counts=counts, ids=ids, params=params)
	return figure


""" callback function for updating funding heat map """
@app.callback(dash.dependencies.Output('funding-heatmap','figure'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])
def callback_funding_heamap(topic_selection, element_selection):
	data = aggregate.funding_by_state(topic=topic_selection, element=element_selection)
	figure = fig.funding_heatmap(data=data)
	return figure


application = app.server
if __name__ == '__main__':
	application.run(debug=True)
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc #import Graph, Input, Dropdown
import dash_html_components as html#import Div, H1, H2, H3, H4, H5, H6, P, A, Span, Big, Main, Button
import plotly.graph_objs as go
import dashapp.figure as fig
import dashapp.aggregate as aggregate
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

mapbox_access_token = r"pk.eyJ1IjoibnJvbWFubzciLCJhIjoiY2ppa2prYjQ2MWszczNsbnh5YnhkZTh1aSJ9.5qBV5E8g3oxlo3ZFL4n6Zw"

# initialize dash app
app = dash.Dash(__name__, 
	server=flaskapp, 
	url_base_pathname='/dashboard/',
	external_scripts=external_scripts,
	external_stylesheets=external_stylesheets
)

app.layout = html.Div(
	className="dash-grid-container grey lighten-3",
	children=[
		html.Div(
			id="filter-panel",
			className="card card-body z-depth-1 pt-2",
			children=[
				html.H4("Filter Options"),
				html.Div(
					className="row",
					children=[
						html.Div(
							className="col text-left",
							children=[
								html.H6("Filter by LTBP research topics."),
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
									placeholder="Select LTBP research topic...",
									value="all",
									searchable=False,
									clearable=False
								)
							]
						),
						html.Div(
							className="col text-left",
							children=[
								html.H6("Filter by bridge element."),
								dcc.Dropdown(
									id="record-set-selection",
									className="text-left",
									options=[
										dict(label="All Bridges & Structures", value="all"),
										dict(label="Bridges: All Elements", value="bridges"),
										dict(label="Untreated Decks", value="untreated_deck"),
										dict(label="Treated Decks", value="treated_deck"),
										dict(label="Joints", value="joints"),
										dict(label="Bearings", value="bearings"),
										dict(label="Coatings", value="coatings")
									],
									placeholder="Select bridge element...",
									value="all",
									searchable=False,
									clearable=False
								)
							]
						),
					],
					style={"margin-bottom":"10px"}
				),
				html.Div(
					className = "row",
					style={"margin-top":"10px"},
					children = [
						html.Div(
							className="col",
							children=[
								html.H6("Filter by Year"),
								html.Div(
									style={"margin-left":"20px","margin-right":"20px"},
									children=[
										dcc.RangeSlider(
											marks={y: f'{y}' for y in range(2006, 2020)},
											min=2006,
											max=2019,
											value=[2014,2019],
											disabled=True
										)
									]
								)
							]
						)
					]
				)
			]
		),
		html.Div(
			id="projects-panel",
			className="card card-body text-center justify-content-center z-depth-1 p-1",
				children=[
				html.H2("{:,d}".format(aggregate.project_count()['total'])),
				html.H3("Projects", className="text-muted")
			]
		),
		html.Div(
			id="publications-panel",
			className="card card-body text-center justify-content-center z-depth-1 p-1",
			children=[
			html.H2("{:,d}".format(aggregate.publication_count())),
			html.H3("Publications", className="text-muted")
			]
		),
		dcc.Graph(
			id='project-count-map',
			className="z-depth-1",
			figure = fig.project_count_map(),
			config={'displayModeBar': False}
		),
		dcc.Graph(
			id='funding-heatmap',
			className="z-depth-1",
			figure=fig.funding_heatmap(),
			config={'displayModeBar': False}
		),
		dcc.Graph(
			id='barchart1',
			className="z-depth-1",
			# figure=fig.bar_chart("attributes"),
			config={'displayModeBar': False}
		),
		dcc.Graph(
			id='barchart2',
			className="z-depth-1",
			# figure=fig.bar_chart("inputs"),
			config={'displayModeBar': False}
		),
		dcc.Graph(
			id='barchart3',
			className="z-depth-1",
			# figure=fig.bar_chart("performance"),
			config={'displayModeBar': False}
		),
		html.H4("Attributes",id="barchart1-heading",className="p-2 text-left h-25"),
		html.H4("Inputs",id="barchart2-heading",className="p-2 text-left h-25"),
		html.H4("Performance",id="barchart3-heading",className="p-2 text-left h-25"),
		html.H4("Count by State",id="project-count-map-heading",className="p-2 text-left"),
		html.H4("Funding by State",id="funding-heatmap-heading",className="p-2 text-left")
	]
)







""" CALLBACKS """

@app.callback(dash.dependencies.Output('projects-panel','children'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])

def callback_project_count(tag, element_tag):
	""" callback function for updating the project count """
	queries = dict(
		tag = tag,
		element_tag = element_tag
	)
	children=[
		html.H2("{:,d}".format(aggregate.project_count(queries = queries)['total'])),
		html.H3("Projects", className="text-muted")
	]
	return children


@app.callback(dash.dependencies.Output('publications-panel','children'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])

def callback_publication_count(tag, element_tag):
	""" callback function for updating the publication count """
	queries = dict(
		tag = tag,
		element_tag = element_tag
	)
	children=[
		html.H2("{:,d}".format(aggregate.publication_count(queries=queries))),
		html.H3("Publications", className="text-muted")
	]
	return children


@app.callback(dash.dependencies.Output('project-count-map','figure'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])

def callback_project_count_map(tag, element_tag):
	""" callback function for updating the project count map """
	queries = dict(
		tag = tag,
		element_tag = element_tag
	)
	data = aggregate.project_count_by_state(queries=queries)
	figure = fig.project_count_map(data=data)
	return figure


@app.callback(dash.dependencies.Output('barchart1','figure'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])

def callback_attribute_barchart(topic_selection, element_selection):
	""" callback function for updating attribute bar chart """

	# format bar labels
	attributes=['construction_quality','design_and_details','material_specifications']
	formatted_attributes=[attr.title().replace("_"," ").replace("And","&") for attr in attributes]
	labels=["<br>".join(textwrap.wrap(label, width=15)) for label in formatted_attributes]

	# get project counts
	counts=[aggregate.project_count_by_topic(topic=attr, 
				element=element_selection, 
				topic_selection=topic_selection) for attr in attributes]

	# generate figure
	figure = fig.bar_chart(labels=labels, counts=counts)

	return figure


@app.callback(dash.dependencies.Output('barchart2','figure'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])

def callback_input_barchart(topic_selection, element_selection):
	""" callback function for updating inputs bar chart """

	# format bar labels
	inputs=['live_load', 'environment', 'maintenance_and_preservation']
	formatted_inputs=[inp.title().replace("_"," ").replace("And","&") for inp in inputs]
	labels=["<br>".join(textwrap.wrap(label, width=15)) for label in formatted_inputs]

	# get project counts
	counts=[aggregate.project_count_by_topic(topic=inp, 
				element=element_selection, 
				topic_selection=topic_selection) for inp in inputs]

	# generate figure
	figure = fig.bar_chart(labels=labels, counts=counts)
	
	return figure


@app.callback(dash.dependencies.Output('barchart3','figure'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])

def callback_performance_barchart(topic_selection, element_selection):
	""" callback function for updating performance bar chart """

	# format bar labels
	performance=['structural_integrity', 'structural_condition', 'functionality', 'cost']
	formatted_performance=[perf.title().replace("_"," ").replace("And","&") for perf in performance]
	labels=["<br>".join(textwrap.wrap(label, width=15)) for label in formatted_performance]

	# get project counts
	counts=[aggregate.project_count_by_topic(topic=perf, 
				element=element_selection, 
				topic_selection=topic_selection) for perf in performance]

	# generate figure
	figure = fig.bar_chart(labels=labels, counts=counts)
	
	return figure


@app.callback(dash.dependencies.Output('funding-heatmap','figure'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])

def callback_heamap(topic_selection, element_selection):
	
	data =aggregate.funding_by_state(topic=topic_selection, element=element_selection)
	figure = fig.funding_heatmap(data=data)

	return figure



# @app.callback(dash.dependencies.Output('funding-heatmap','figure'),[dash.dependencies.Input('tags-selection','value')])
# def updateHeatMap(selection):
# 	if selection == 'all' or selection == "":
# 		query = None
# 	else:
# 		query = selection
# 	data = aggregate.funding_by_state(query=query)
# 	figure = fig.funding_heatmap(data=data)
# 	return figure







application = app.server
if __name__ == '__main__':
	application.run(debug=True)
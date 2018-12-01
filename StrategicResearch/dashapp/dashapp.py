# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
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

# initialize dash app
app = dash.Dash(__name__, 
	server=flaskapp, 
	url_base_pathname='/dashboard/',
	external_scripts=external_scripts,
	external_stylesheets=external_stylesheets
)
app.config.suppress_callback_exceptions = True
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

""" ----------------------------- DASHBOARD -------------------------------- """
dashboard_layout = html.Div([
	html.Div(
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
				# figure=fig.funding_heatmap(),
				config={'displayModeBar': False}
			),
			dcc.Graph(
				id='barchart1',
				className="z-depth-1",
				config={'displayModeBar': False}
			),
			dcc.Graph(
				id='barchart2',
				className="z-depth-1",
				config={'displayModeBar': False}
			),
			dcc.Graph(
				id='barchart3',
				className="z-depth-1",
				config={'displayModeBar': False}
			),
			html.H4("Attributes",id="barchart1-heading",className="p-2 text-left h-25"),
			html.H4("Inputs",id="barchart2-heading",className="p-2 text-left h-25"),
			html.H4("Performance",id="barchart3-heading",className="p-2 text-left h-25"),
			html.H4("Count by State",id="project-count-map-heading",className="p-2 text-left"),
			html.H4("Funding by State",id="funding-heatmap-heading",className="p-2 text-left"),
			# html.Button(children=[dcc.Link('Redirect', href='/explore')], id='barchart1-projects-button',className="p-1 text-center h-20 btn btn-light btn"),
			# html.A('redirect', 
				# id='barchart1-publications-button',
				# className="p-1 text-center h-20 btn btn-light btn",
			# 	href="http://127.0.0.1:5000/", 
			# 	target="_blank")
		]
	)
])


""" callback function for redirecting user on performance barchart click """
@app.callback(
        dash.dependencies.Output('barchart3-heading', 'children'),
        [dash.dependencies.Input('barchart3', 'clickData')])
def on_attr_click(selection):
	if selection is None:
		return "Test"
	else:
		print(len(selection['points'][0]['customdata']))
		return "Test"


""" callback function for redirecting user on input barchart click """
@app.callback(
        dash.dependencies.Output('barchart2-heading', 'children'),
        [dash.dependencies.Input('barchart2', 'clickData')])
def on_attr_click(selection):
	if selection is None:
		return "Test"
	else:
		print(len(selection['points'][0]['customdata']))
		return "Test"


""" callback function for redirecting user on attr barchart click """
@app.callback(
        dash.dependencies.Output('barchart1-heading', 'children'),
        [dash.dependencies.Input('barchart1', 'clickData')])
def on_attr_click(selection):
	if selection is None:
		return "Test"
	else:
		print(len(selection['points'][0]['customdata']))
		return "Test"


""" callback function for redirecting user on map click """
@app.callback(
        dash.dependencies.Output('project-count-map-heading', 'children'),
        [dash.dependencies.Input('project-count-map', 'clickData')])
def on_map_click(selection):
	if selection is None:
		return "Test"
	else:
		print(len(selection['points'][0]['customdata']))
		return selection['points'][0]['text']


""" callback function for updating the project count """
@app.callback(dash.dependencies.Output('projects-panel','children'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])
def callback_project_count(tag, element_tag):
	queries = dict(tag=tag, element_tag=element_tag)
	children=[
		html.H2("{:,d}".format(aggregate.project_count(queries = queries)['total'])),
		html.H3("Projects", className="text-muted")
	]
	return children


""" callback function for updating the publication count """
@app.callback(dash.dependencies.Output('publications-panel','children'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])
def callback_publication_count(tag, element_tag):
	queries = dict(tag=tag, element_tag=element_tag)
	children=[
		html.H2("{:,d}".format(aggregate.publication_count(queries=queries))),
		html.H3("Publications", className="text-muted")
	]
	return children


""" callback function for updating the project count map """
@app.callback(dash.dependencies.Output('project-count-map','figure'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])
def callback_project_count_map(tag, element_tag):
	queries = dict(tag=tag, element_tag=element_tag)
	data = aggregate.project_count_by_state(queries=queries)
	figure = fig.project_count_map(data=data)
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
	# generate figure
	figure = fig.bar_chart(labels=labels, counts=counts, ids=ids)
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
	# generate figure
	figure = fig.bar_chart(labels=labels, counts=counts, ids=ids)
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
	# generate figure
	figure = fig.bar_chart(labels=labels, counts=counts, ids=ids)
	return figure


""" callback function for updating funding heat map """
@app.callback(dash.dependencies.Output('funding-heatmap','figure'),
	[dash.dependencies.Input('tags-selection','value'),
		dash.dependencies.Input('record-set-selection','value')])
def callback_funding_heamap(topic_selection, element_selection):
	data = aggregate.funding_by_state(topic=topic_selection, element=element_selection)
	figure = fig.funding_heatmap(data=data)
	return figure



""" ------------------------------ RESULTS --------------------------------- """

results_layout = html.Div([
    html.H3('Results'),
    dcc.Dropdown(
        id='app-1-dropdown',
        options=[
            {'label': 'App 1 - {}'.format(i), 'value': i} for i in [
                'NYC', 'MTL', 'LA'
            ]
        ]
    ),
    html.Div(id='app-1-display-value'),
    html.A('Back', href='http://127.0.0.1:5000/analyze'),
    dcc.Link('Go to Record', href='/dashboard/results/record')
])

@app.callback(dash.dependencies.Output('app-1-display-value', 'children'),
    			[dash.dependencies.Input('app-1-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)



""" ------------------------------- RECORD --------------------------------- """

record_layout = html.Div([
    html.H2('Record'),
    dcc.Input(id='input-1-state', type='text', value='Montreal'),
    dcc.Input(id='input-2-state', type='text', value='Canada'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-state'),
    html.Br(),
    dcc.Link('Back', href='/dashboard/results'),
])

@app.callback(dash.dependencies.Output('output-state', 'children'),
              [dash.dependencies.Input('submit-button', 'n_clicks')],
              [dash.dependencies.State('input-1-state', 'value'),
               dash.dependencies.State('input-2-state', 'value')])
def update_output(n_clicks, input1, input2):
    return ('The Button has been pressed {} times,'
            'Input 1 is "{}",'
            'and Input 2 is "{}"').format(n_clicks, input1, input2)




""" callback function for redirecting to other apps """
@app.callback(dash.dependencies.Output('page-content', 'children'), 
				[dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
	print(pathname)
	if pathname == '/dashboard/' :
		return dashboard_layout
	elif pathname == '/dashboard/results':
		return results_layout
	elif pathname == '/dashboard/results/record':
		return record_layout
	else:
		return '404'


application = app.server
if __name__ == '__main__':
	application.run(debug=True)
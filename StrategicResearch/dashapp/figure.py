import dashapp.aggregate as aggregate
import plotly.graph_objs as go
import json
import os

with open("./dashapp/app/static/statesGeo.json") as f:
	geo = json.load(f)

# states geo JSON
# def getStatesGeo():
# 	with open('./statesGeo.json','r') as f:
# 		geo = json.load(f)
# 	return geo


def project_count_map(data=None, params=None):

	MAPBOX_ACCESS_TOKEN = r"pk.eyJ1IjoibnJvbWFubzciLCJhIjoiY2ppa2prYjQ2MWszczNsbnh5YnhkZTh1aSJ9.5qBV5E8g3oxlo3ZFL4n6Zw"
	STATES_SHAPEFILE_PATH = r"./dashapp/app/static/geojson"
	BINS = {
		range(0, 1): [], range(1, 5): [], range(5, 10): [],
		range(10, 15): [], range(15, 20): [], range(20, 25): [],
		range(25, 30): [], range(30, 35): [], range(35, 40): [],
		range(40, 45): [], range(45, 50): [], range(50, 200): []
	}
	COLORSCALE = [
		"#ffffff", "#eeeeee", "#e0e0e0",
		"#bdbdbd", "#deebf7", "#c6dbef",
		"#9ecae1", "#6baed6", "#4292c6",
		"#2171b5", "#08519c", "#08306b"
	]

	# retrieve data if none provided
	if data == None:
		data = aggregate.project_count_by_state()

	# bins, bin counts, and bin colors
	colormap = dict(zip(BINS, COLORSCALE))
	for item in list(data.items()):
		for key in BINS:
			if item[1].get('doc_count') in key:
				BINS[key].append(item[0])

	# get list of states with data
	states_with_data = []
	[states_with_data.append(s) for l in BINS.values() for s in l]

	# legend set up
	annotations = []
	for i, bin in enumerate(BINS):
		annotations.append(
			dict(
				arrowcolor=colormap[bin],
				arrowhead=0,
				arrowwidth=10,
				align='left',
				ax=-60,
				ay=0,
				bgcolor='#FFFFFF',
				font=dict(
					family='Courier New, monospace', 
					size=14
				),
				text=f"{min(bin)} - {max(bin)}" if min(bin) != max(bin) else f"{min(bin)}",
				x=0.13,
				y=0.75-(i/20)
			)
		)

	# set up map layout
	layout = dict(		
		annotations=annotations,
		hovermode="closest",
		hoverlabel=dict(
			bgcolor='#3E4551'
		),
		mapbox=dict(
			accesstoken=MAPBOX_ACCESS_TOKEN,
			center=dict(
				lat=39, 
				lon=-99
			),
			layers=[],
			pitch=0,
			style='light',
			zoom=3.0,
		),
		margin=dict(
			l=0.01,
			r=0.01,
			t=0.01,
			b=0.01
		),
		paper_bgcolor='rgba(0,0,0,0)',
    	plot_bgcolor='rgba(0,0,0,0)'
	)

	# set up layers for states 
	text, lat, lon, customdata = [], [], [], []
	for f1 in os.listdir(STATES_SHAPEFILE_PATH):

		# get state shape file
		with open(os.path.join(STATES_SHAPEFILE_PATH, f1), 'r') as f2:
			state_shapefile = json.load(f2)

		# for each state
		state = f1.split(".")[0]

		# append lat/lon data points
		lat.append(geo[state]['latitude'])
		lon.append(geo[state]['longitude'])

		# append customdata
		if data.get(state):
			customdata.append(data.get(state).get('doc_ids'))
		else:
			customdata.append(None)

		# append hovertext
		if data.get(state):
			count = data.get(state).get('doc_count')
		else:
			count = 0
		hovertext = (f"{geo[state]['full']}<br>" +
					 f"<a href='/analyze/results?state={state}&{params}' target='_blank'>" +
					 f"Total Projects</a>: {count}")
		text.append(hovertext)

		# append geolayers to layout
		if state in states_with_data:
			for b in BINS:
				if state in BINS[b]:
					color = colormap[b]
					geo_layer = dict(
						color=color,
						opacity=0.6,
						sourcetype='geojson',
						source=state_shapefile,
						type='fill'
					)
					layout['mapbox']['layers'].append(geo_layer)
		else:
			color = COLORSCALE[0]
			geo_layer = dict(
				
				color=color,
				opacity=0.7,
				sourcetype='geojson',
				source=state_shapefile,
				type='fill'
			)
			layout['mapbox']['layers'].append(geo_layer)

	# create trace dict for layers
	trace = dict(
		customdata=customdata,
		hoverinfo="text",
		lat=lat,
		lon=lon,
		marker=dict(size=20, color='white', opacity=0),
		text=text,
		type='scattermapbox'
	)

	figure = dict(data=[trace], layout=layout)
	return figure

def bar_chart(labels, counts, ids, params=None):


	# set up trace
	trace = go.Bar(
		hoverinfo="none",
		customdata=[id for id in ids],
		insidetextfont=dict(
			color="black",
			size=15
		),
		marker=dict(color="#3F729B"),
		outsidetextfont=dict(
			color="black",
			size=15
		),
		text=[f"<a href='/analyze/results?{params[i]}' target='_blank' style='color:black'>{count}</a>" for i, count in enumerate(counts)],
		textposition="auto",
		x=labels,
		y=counts
	)

	# set up layout
	layout = go.Layout(
		margin={'l': 10, 'r': 10, 't': 50, 'b': 40, },
		paper_bgcolor='rgba(0,0,0,0)',
    	plot_bgcolor='rgba(0,0,0,0)',
		xaxis=dict(showticklabels=True),
		yaxis=dict(showgrid=False, showticklabels=False)
	)

	figure = go.Figure(data=[trace], layout=layout)

	return figure




def funding_heatmap(data=None):

	# retrieve data and remove 'DC'
	if not data:
		data = aggregate.funding_by_state(topic="all", element="all")
	states = [state for state in data.keys() if (state != 'DC') and (
		sum([b["doc_count"] for b in list(data[state].values())]) != 0)]
	# state_labels = [geo[state.upper()]['abbrv'] if len(state) == 2 else geo[state]['abbrv'] finally state for state in states]

	# filter

	# format data for heatmap
	X = states
	Y = ["$<100k", "$100-250k", "$250-500k", "$500-750k", "$750k-1M", "$1M+"]
	Z = []
	buckets = ['0.0-100000.0', '100000.0-250000.0', '250000.0-500000.0',
			   '500000.0-750000.0', '750000.0-1000000.0', '1000000.0-*']
	for b in buckets:
		z = []
		for state in states:
			z.append(data[state][b]['doc_count'])
		Z.append(z)

	# format hover text for heatmap
	hovertext = []
	xx, yy = [], []
	for yi, amount in enumerate(Y):
		hovertext.append([])
		for xi, state in enumerate(X):
			# if xi == 0 and yi == 0:
			hovertext[-1].append(
				(f"State:  {state}<br>" +
					f"Dollar Amount: {amount}<br>"+ 
					f"<a href='/analyze/results?state=all&all' target='_blank'>" +
					f"Project Count</a> :  {Z[yi][xi]}")
			)
			xx.append(xi)
			yy.append(yi)
			# else:
			# 	hovertext[-1].append(
			# 		(f"State:  {xx}<br>" +
			# 			f"Dollar Amount: {yy}<br>"+ 
			# 			f"Project Count:  {Z[yi][xi]}"))

	trace1 = go.Heatmap(
		z=Z,
		x=X,
		y=Y,
		# opacity=0.95,
		ygap=1,
		xgap=1,
		colorscale=[[0, 'rgb(230, 234, 237)'], [1, 'rgb(15,82,186)']],
		colorbar=dict(
			thickness=15,
			x=1.01,
			xpad=0,
			ypad=0
		),
		hoverinfo='text',
		text=hovertext
	)

	trace2 = go.Scatter(
		x=X,
		y=[Y]*len(states),
		mode="markers",
		marker=dict(size= 14,
                    line= dict(width=1),
                    opacity= 0.3,
                   ),
		# text=hovertext
	)

	layout = go.Layout(
		xaxis=dict(title="States"),
		yaxis=dict(
			title="Funding (Dollar Amount)",
			tickprefix="  "
		),
		margin={'l': 110, 'r': 10, 't': 50, 'b': 70, },
		hovermode='closest',
		hoverdistance=1,
		spikedistance=1,
	)

	figure = go.Figure(data=[trace1], layout=layout)

	return figure



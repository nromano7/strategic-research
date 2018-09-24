import dashapp.aggregate as aggregate
import plotly.graph_objs as go
import json
import os
import textwrap

# states geo JSON
def getStatesGeo():
	with open('./statesGeo.json','r') as f:
		geo = json.load(f)
	return geo

def project_count_map(data=None):

  mapbox_access_token = r"pk.eyJ1IjoibnJvbWFubzciLCJhIjoiY2ppa2prYjQ2MWszczNsbnh5YnhkZTh1aSJ9.5qBV5E8g3oxlo3ZFL4n6Zw"
  state_shapefile_PATH = r"./dashapp/app/static/geojson"
  with open("./dashapp/app/static/statesGeo.json") as f:
    geo = json.load(f)

  if data == None:
    data = aggregate.project_count_by_state()

  BINS = {
    range(0,1):[],
    range(1,5):[],
    range(5,10):[],
    range(10,15):[],
    range(15,20):[],
    range(20,25):[],
    range(25,30):[],
    range(30,35):[],
    range(35,40):[],
    range(40,45):[],
    range(45,50):[],
    range(50,200):[]
  }

  COLORSCALE = [
    "#ffffff",
    "#eeeeee",
    "#e0e0e0",
    "#bdbdbd",
    "#deebf7",
    "#c6dbef",
    "#9ecae1",
    "#6baed6",
    "#4292c6",
    "#2171b5",
    "#08519c",
    "#08306b"
  ]
  colormap = dict(zip(BINS, COLORSCALE))
  [BINS[key].append(item[0]) for key in BINS for item in list(data.items()) if item[1] in key]
    
  layout = go.Layout(
    mapbox = dict(
      layers = [],
      accesstoken = mapbox_access_token,
      style='light',
      center=dict(
        lat=38.72490,
        lon=-95.71446
      ),
      pitch=0,
      zoom=3.1,
    ),
    hovermode="closest",
    hoverlabel = dict(
      bgcolor = '#3E4551'
    ),
    margin = dict(
      l=0.01,
      r=0.01,
      t=0.01,
      b=0.01
    )
  )
       
  text, lat, lon = [], [], []
  for f1 in os.listdir(state_shapefile_PATH):

    state = f1.split(".")[0]
    
    lat.append(geo[state]['latitude'])
    lon.append(geo[state]['longitude'])
    hovertext = (f"{geo[state]['full']}" +
      f"<br>Project Count: {data.get(state)}")
    text.append(hovertext)

    with open(os.path.join(state_shapefile_PATH,f1),'r') as f2:
      state_shapefile = json.load(f2)

    states_with_data = []
    [states_with_data.append(s) for l in BINS.values() for s in l]
    if state in states_with_data:
      for b in BINS:
        if state in BINS[b]:
          color = colormap[b]
          geo_layer = dict(
            sourcetype = 'geojson',
            source = state_shapefile,
            type = 'fill',
            color = color,
            opacity = 0.6
          )
          layout['mapbox']['layers'].append(geo_layer)
    else:
      color = COLORSCALE[0]
      geo_layer = dict(
        sourcetype = 'geojson',
        source = state_shapefile,
        type = 'fill',
        color = color,
        opacity = 0.7
      )
      layout['mapbox']['layers'].append(geo_layer)

  # figure['data'][0]['lat'] = lat
  # figure['data'][0]['lon'] = lon
  # figure['data'][0]['text'] = text

  trace = go.Scattermapbox(
    lat=lat,
    lon=lon,
    text=text,   
    hoverinfo="text",
    marker = dict(size=20, color='white', opacity=0)
  )

  go_data = go.Data([trace])

 

  figure = go.Figure(data=go_data, layout=layout)

  return figure

def funding_heatmap(data=None):

  # retrieve data and remove 'DC'
  if not data:
    data = aggregate.funding_by_state()
  states = [state for state in data.keys() if (state != 'DC') and (sum([b["doc_count"] for b in list(data[state].values())]) != 0)]

  #filter

  # format data for heatmap
  X = states
  Y = ["$<100k", "$100-250k", "$250-500k", "$500-750k", "$750k-1M", "$1M+"]
  Z = []
  buckets = ['0.0-100000.0','100000.0-250000.0','250000.0-500000.0','500000.0-750000.0','750000.0-1000000.0','1000000.0-*']
  for b in buckets:
    z = []
    for state in states:
      z.append(data[state][b]['doc_count'])
    Z.append(z)

  # format hover text for heatmap
  hovertext = []
  for yi, yy in enumerate(Y):
    hovertext.append([])
    for xi, xx in enumerate(X):
      hovertext[-1].append(f'State:  {xx}<br />Dollar Amount:  {yy}<br />Project Count:  {Z[yi][xi]}')

  trace = go.Heatmap(
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

  data = go.Data([trace])

  layout = go.Layout(
            xaxis=dict(title="States"),
            yaxis=dict(
              title="Funding (Dollar Amount)",
              tickprefix="  "
            ),
            margin={'l':110,'r':10,'t':50,'b':70,},
          )
  
  figure = go.Figure(data=data, layout=layout)
 
  return figure

def bar_chart(category, data=None):

  categories=dict(
    attributes=['construction_quality','design_and_details','material_specifications'],
    inputs=['live_load', 'environment', 'maintenance_and_preservation'],
    performance=['structural_integrity', 'structural_condition', 'functionality', 'cost']
  )

  tags=[tag.title().replace("_"," ").replace("And","&") for tag in categories.get(category)]
  labels=["<br>".join(textwrap.wrap(tag,width=15)) for tag in tags]
  counts=[aggregate.project_count_by_tag(tag) for tag in categories.get(category)]

  trace = go.Bar(
    x=labels,
    y=counts,
    text=[label for label in labels],
    textposition="auto",
    # opacity=0.9,
    marker=dict(color="#3F729B"),
    hoverinfo="text",
    hovertext=counts,
    insidetextfont=dict(
      color="black",
      size=13
    ),
    outsidetextfont=dict(
      color="black",
      size=13
    ),
  )

  data = [trace]

  layout = go.Layout(
    margin={'l':35,'r':25,'t':50,'b':15,},
    xaxis=dict(showticklabels=False),
    # plot_bgcolor='rgba(0,0,0,0)',
    # paper_bgcolor='rgba(0,0,0,0)'
  )


  figure = go.Figure(data=data, layout=layout)

  return figure
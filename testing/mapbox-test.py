import itertools
import json
import os
import aggregations.aggs as aggs

mapbox_access_token = r"pk.eyJ1IjoibnJvbWFubzciLCJhIjoiY2ppa2prYjQ2MWszczNsbnh5YnhkZTh1aSJ9.5qBV5E8g3oxlo3ZFL4n6Zw"
state_shapefile_PATH = r"./StrategicResearchApp/app/static/geojson"

with open("./StrategicResearchApp/statesGeo.json") as f:
  geo = json.load(f)

data = aggs.ProjectCountByState()

# BIN_RANGES = [
#   "0-4",
#   "5-9",
#   "10-15",
#   "16-20",
#   "21-25",
#   "26-30",
#   "31-35",
#   "36-40",
#   "41-45",
#   "46-50",
#   "50+"
# ]

BINS = {
  range(0,5):[],
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
  '#2a4858',
  '#235a6b',
  '#106e7c',
  '#008287',
  '#00968e',
  '#27a990',
  '#49bd8c',
  '#73ce85',
  '#9cdf7c',
  '#caee74',
  '#fafa6e'
]

colormap = dict(zip(BINS, COLORSCALE))
[BINS[key].append(item[0]) for key in BINS for item in list(data.items()) if item[1] in key]
  
figure = dict(
  data=[
    dict(
      type='scattermapbox',
      hoverinfo="text",
      marker = dict(size=20, color='white', opacity=0)
    )
  ],
  layout=dict(
    mapbox = dict(
      layers = [],
      accesstoken = mapbox_access_token,
      style='light',
      center=dict(
        lat=38.72490,
        lon=-95.61446
      ),
      pitch=0,
      zoom=3.1
    ),
    hovermode="closest",
    margin = dict(
      l=0.01,
      r=0.01,
      t=0.01,
      b=0.01
    )
  )
)

    
text, lat, lon = [], [], []
for f1 in os.listdir(state_shapefile_PATH):

  state = f1.split(".")[0]
  
  lat.append(geo[state]['latitude'])
  lon.append(geo[state]['longitude'])
  hovertext = f"{geo[state]['full']} <br> Projects: {data.get(state)}"
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
          opacity = 0.5
        )
        figure['layout']['mapbox']['layers'].append(geo_layer)
  else:
    color = COLORSCALE[0]
    geo_layer = dict(
      sourcetype = 'geojson',
      source = state_shapefile,
      type = 'fill',
      color = color,
      opacity = 0.5
    )
    figure['layout']['mapbox']['layers'].append(geo_layer)

figure['data'][0]['lat'] = lat
figure['data'][0]['lon'] = lon
figure['data'][0]['text'] = text

from plotly.offline import plot
import plotly.graph_objs as go

plot(figure)

  
  # all_coordinates = state_shapefile['features'][0]['geometry']['coordinates']
  
  # flattened = lambda x: [True if len(l) == 2 else False for l in x]
  
  # # while not all(l == True for l in flattened(all_coordinates)):
  #   all_coordinates = list(itertools.chain.from_iterable(all_coordinates))

  # for coord in all_coordinates:
  #   lat.append(coord[0])
  #   lon.append(coord[1])
  #   states.append(state)

# with open(shapefile_PATH) as f:
#   sf = json.load(f)

# with open("./StrategicResearchApp/statesGeo.json") as f:
#   geo = json.load(f)

# states = []
# for s in sf['features']:
  
#   state = s["properties"]["NAME"]
#   states.append(state)
#   abbrv = geo[state]["abbrv"]
#   coordinates = s["geometry"]["coordinates"]

#   geo[state]["coordinates"] = coordinates[0]
#   geo[abbrv]["coordinates"] = coordinates[0]

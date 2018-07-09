import itertools
import json
import os

mapbox_access_token = r"pk.eyJ1IjoibnJvbWFubzciLCJhIjoiY2ppa2prYjQ2MWszczNsbnh5YnhkZTh1aSJ9.5qBV5E8g3oxlo3ZFL4n6Zw"
state_shapefile_PATH = r"./StrategicResearchApp/app/static/geojson"

with open("./StrategicResearchApp/statesGeo.json") as f:
  geo = json.load(f)
  
figure = dict(
  data=[
    dict(
      type='scattermapbox',
      hoverinfo="text",
      marker = dict(size=10, color='white', opacity=0)
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

states, lat, lon = [], [], []
for f1 in os.listdir(state_shapefile_PATH):

  state = f1.split(".")[0]
  
  lat.append(geo[state]['latitude'])
  lon.append(geo[state]['longitude'])
  states.append(state)

  with open(os.path.join(state_shapefile_PATH,f1),'r') as f2:
    state_shapefile = json.load(f2)

  geo_layer = dict(
    sourcetype = 'geojson',
    source = state_shapefile,
    type = 'fill',
    color = "blue",
    opacity = 0.4
  )

  figure['layout']['mapbox']['layers'].append(geo_layer)

figure['data'][0]['lat'] = lat
figure['data'][0]['lon'] = lon
figure['data'][0]['text'] = states

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

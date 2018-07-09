import json

shapefile_PATH = r"./files/shapefile_large.json"

with open(shapefile_PATH) as f:
  sf = json.load(f)

with open("./StrategicResearchApp/statesGeo.json") as f:
  geo = json.load(f)

for s in sf['features']:

  state = s["properties"]["NAME"]
  abbrv = geo[state]["abbrv"]

  state_shape = {
    "type": "FeatureCollection",
    "features":[
      s
    ]
  }

  with open(f"./StrategicResearchApp/app/static/geojson/{abbrv}.json",'w') as f:
    json.dump(state_shape,f)



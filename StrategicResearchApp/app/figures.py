from app import getStatesGeo
import app.aggregations as aggs
import json
import os
import plotly.graph_objs as go

def FundingLevelHeatMap(data=None):

  # retrieve data and remove 'DC'
  if not data:
    data = aggs.FundingLevelByState()
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

  figure = {
    'data': [
      go.Heatmap(
        z=Z,
        x=X,
        y=Y,
        opacity=0.95,
        ygap=1,
        xgap=1,
        colorscale=[[0, 'rgb(244, 246, 247)'], [1, 'rgb(15,82,186)']],
        colorbar=dict(
          thickness=15,
          x=1.01,
          xpad=0,
          ypad=0
        ),
        hoverinfo='text',
        text=hovertext
      )
    ],
    'layout': 
      go.Layout(
        xaxis=dict(
          title="States"
        ),
        yaxis=dict(
          title="Funding (Dollar Amount)",
          tickprefix="  "
        ),
        margin={'l':110,'r':10,'t':30,'b':70,},
      )
  }
  
  return figure

def ProjectCountMap1(data=None):

  if not data:
    data = aggs.ProjectCountByState()

  states = [state for state in data.keys() if state != 'DC']
  counts = [data[state] for state in states]

  colorscale=[
    [0,'rgb(255,255,217)'],
    [0.1,'rgb(237,248,177)'],
    [0.2,'rgb(199,233,180)'],
    [0.35,'rgb(127,205,187)'],
    [0.45,'rgb(65,182,196)'],
    [0.6,'rgb(29,145,192)'],
    [0.75,'rgb(34,94,168)'],
    [0.9,'rgb(37,52,148)'],
    [1,'rgb(8,29,88)']
  ]

  figure = {
    'data':[
      dict(
        type='choropleth',
        # autocolorscale = True,
        colorscale=colorscale,
        showscale=False,
        opacity=0.9,
        locations = states, 
        z = counts, 
        locationmode = 'USA-states',
        marker = dict(line = dict(color='rgb(255,255,255)',width=0.5)),
        colorbar = dict(
          title = "Project Count",
          x = 1,
          xanchor = 'left',
          xpad = 0
        )
      )
    ],
    'layout':dict(
      # margin={
      #   'l':0,
      #   'r':0,
      #   'b':0,
      #   't':0,
      #   'pad':10
      # },
      geo = dict(
        scope='usa',
        # projection=dict( type='albers usa' ),
        showlakes = True,
        # lakecolor = 'rgb(255, 255, 255)'
      ),
    )
  }

  return figure

def ProjectCountMap2(data=None):

  mapbox_access_token = r"pk.eyJ1IjoibnJvbWFubzciLCJhIjoiY2ppa2prYjQ2MWszczNsbnh5YnhkZTh1aSJ9.5qBV5E8g3oxlo3ZFL4n6Zw"
  state_shapefile_PATH = r"./app/static/geojson"

  with open("./statesGeo.json") as f:
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

  return figure

def FundingByYearHistogram(data=None):

  if not data:
    data = aggs.FundingByYear()

  x = [x for x in data]
  y = [data[i] for i in x]

  figure=dict(
    data=[
      dict(
        x=x,
        y=y,
        type='bar',
      )
    ],
    layout=dict(
      margin=dict(
        l=40,
        r=20,
        b=20,
        t=60,
      ),
      title="Funding By Year",
      titlefont=dict(
        size=30
      )
    )
  )
  
  return figure

def ProjectCountByYearHistogram(data=None):
  
  if not data:
    data = aggs.ProjectCountByYear()
    
  x = [x for x in data]
  y = [data[i] for i in x]

  figure=dict(
    data=[
      dict(
        x=x,
        y=y,
        type='bar',
      )
    ],
    layout=dict(
      margin=dict(
        l=40,
        r=20,
        b=20,
        t=60,
      ),
      title="Project Count By Year",
      titlefont=dict(
        size=30
      )
    )
  )
  
  return figure

def TermsPieChart():

  data = aggs.LTBPTermsCount()
  labels = [key for key in data]
  values = [data[key] for key in data]

  figure = {
    "data": [
      {
        "values": values,
        "labels": labels,
        "domain":dict(column=60),
        # "hoverinfo":"label",
        "hole": .4,
        "type": "pie",
        "textinfo":"text+percent",
        "text":labels,
        # "textposition":"outside",
        "showlegend":False,
        "marker":dict(
          colors='Viridis'
        )
      }],
    "layout": {
      "annotations": [
        dict(
          font=dict(
            size=30
          ),
          text="LTBP Terms",
          x=0.5,
          y=0.5,
          # bgcolor="rgb(256,256,256,1)",
          # bordercolor="#000000",
          showarrow=False
        )
      ],
      "legend":dict(
        orientation='h',
        xanchor="center",
        yanchor="bottom",
        x=0.5,
        y=1
      ),
      "margin":dict(
        l=10,
        r=10,
        b=20,
        t=20
      ),
      "titlefont":dict(
        size=30
      )

    }
  }

  return figure

def TermsBarChart():

  data = aggs.LTBPTermsCount()
  sorted_data = sorted(data, key=data.get)
  labels = [key for key in sorted_data]
  values = [data[key] for key in sorted_data]
  total_projects=sum(values)
  percents = ["{:.2%}".format(val/total_projects) for val in values]

  figure = dict(
    data=[
      dict(
        type='bar',
        x=values,
        text=[" "+label+" " for label in labels],
        textposition="auto",
        orientation='h',
        opacity=0.8,
        hoverinfo="text",
        hovertext=percents,
        insidetextfont=dict(
          color="black",
          size=15
        ),
        outsidetextfont=dict(
          color="black",
          size=15
        ),
        cliponaxis=False,
        marker=dict(
          # color=[[0, 'rgb(244, 246, 247)'], [1, 'rgb(15,82,186)']],
          colorscale=[[0, 'rgb(244, 246, 247)'], [1, 'rgb(15,82,186)']],
          cmin=0,
          cmax=1,
          line=dict(
            width=1,
            color="black",
          )
        )
      )
    ],
    layout=dict(
      # annotations=dict(
      #   x=300,
      #   y=1,
      #   xref='x',
      #   yref='y',
      #   bgcolor="black",
      #   text="labels"
      # ),
      # xaxis=dict(
      #   title="Project Count",
      #   tickprefix="  "
      # ),
      yaxis=dict(
        showticklabels=False,
      ),
      margin=dict(
        l=10,
        r=10,
        t=10,
        b=20
      )
    )
  )
  
  return figure


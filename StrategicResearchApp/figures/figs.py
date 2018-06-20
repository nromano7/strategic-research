import sys
import os
sys.path.append(os.getcwd())

from aggregations import aggs
import json
import plotly.graph_objs as go

def FundingLevelHeatMap():

  data = aggs.FundingLevelByState()
  states = [state for state in data.keys() if state != 'DC']
  X = states
  Y = ["$<100k", "$100-250k", "$250-500k", "$500-750k", "$750k-1M", "$1M+"]
  buckets = ['0.0-100000.0','100000.0-250000.0','250000.0-500000.0','500000.0-750000.0','750000.0-1000000.0','1000000.0-*']
  Z = []
  for b in buckets:
    z = []
    for state in states:
      z.append(data[state][b]['doc_count'])
    Z.append(z)

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
        colorbar={'thickness':15,'x':1.01, 'xpad':0, 'ypad':0,},
        hoverinfo='text',
        text=hovertext
      )
    ],
    'layout': 
      go.Layout(
        # title = 'Funding by State',
        xaxis={'title': 'States'},
        yaxis={'title': 'Funding (Dollar Amount)','tickprefix':"  "},
        margin={'l':110,'r':40,'t':30,'b':70,},
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
      margin={
        'l':0,
        'r':0,
        'b':0,
        't':0,
        'pad':0
      },
      geo = dict(
        scope='usa',
        # projection=dict( type='albers usa' ),
        showlakes = True,
        # lakecolor = 'rgb(255, 255, 255)'
      ),
    )
  }

  return figure

def ProjectCountMap2():

  mapbox_access_token = "pk.eyJ1IjoibnJvbWFubzciLCJhIjoiY2ppa2prYjQ2MWszczNsbnh5YnhkZTh1aSJ9.5qBV5E8g3oxlo3ZFL4n6Zw"
  
  with open('./files/statesGeo.json','r') as f:
    geo = json.load(f)

  BINS = [
    '0-10',
    '11-20',
    '21-20',
    '20-25',
    '25-30',
    '30-35',
    '35-40',
    '40-45',
  ]

  # hovertext = []
  # for 

  data = aggs.ProjectCountByState()
  states = [state for state in data.keys() if state != 'DC']
  counts = [data[state] for state in states]
  latitude = [geo[state]['latitude'] for state in states]
  longitude = [geo[state]['longitude'] for state in states]
  figure = {
    'data':[
      dict(
        type='scattermapbox',
        lat = latitude,
        lon = longitude,
        hoverinfo='text',
        text=states
      )
    ],
    'layout':dict(
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
      margin = dict(
        l=10,
        r=10,
        b=10,
        t=10
      )
    )
  }

  return figure

def FundingByYearHistogram():

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
        "hoverinfo":"label",
        "hole": .4,
        "type": "pie",
        # "textinfo":"text+percent",
        # "text":labels,
        "textposition":"outside",
        "showlegend":True,
        "marker":dict(
          colors='Viridis'
        )
      }],
    "layout": {
      "title":"LTBP Terms",
      # "annotations": [
      #   {
      #     "font": {
      #         "size": 30
      #     },
      #     "showarrow": False,
      #     # "text": "LTBP Terms",
      #     "x": 0.5,
      #     "y": 0.5
      #   }
      # ],
      "legend":dict(orientation='h'),
      "margin":dict(
        l=10,
        r=10,
        b=10,
        t=60
      ),
      "titlefont":dict(
        size=30
      )

    }
  }

  return figure




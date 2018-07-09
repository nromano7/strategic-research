from app import getStatesGeo
import app.aggregations as aggs
import json
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

  mapbox_access_token = "pk.eyJ1IjoibnJvbWFubzciLCJhIjoiY2ppa2prYjQ2MWszczNsbnh5YnhkZTh1aSJ9.5qBV5E8g3oxlo3ZFL4n6Zw"
  
  geo = getStatesGeo()

  # data = aggs.ProjectCountByState()
  # states = [state for state in data.keys() if state != 'DC']
  # counts = [data[state] for state in states]
  # latitude = [geo[state]['latitude'] for state in states]
  # longitude = [geo[state]['longitude'] for state in states]
  figure = {
    'data':[
      dict(
        type='scattermapbox',
      #   lat = [], #latitude,
      #   lon = [], #longitude,
      #   hoverinfo='text',
      #   text=states
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
        l=0.01,
        r=0.01,
        t=0.01,
        b=0.01
      )
    )
  }

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


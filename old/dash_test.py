# -*- coding: utf-8 -*-
import dash
from dash_core_components import Graph
from dash_html_components import Div, H1
import plotly.graph_objs as go
import plotly.figure_factory as ff
import json

with open('./files/heatmap_res.json', 'r') as f:
  res = json.load(f)

states = res['aggregations']['agencies']['states']['buckets']
states = [state for state in states if state.get('key') != 'DC']
X = []
ranges = ['0.0-100000.0','100000.0-250000.0','250000.0-500000.0','500000.0-750000.0','750000.0-1000000.0','1000000.0-*']
Y = ["$<100k", "$100-250k", "$250-500k", "$500-750k", "$750k-1M", "$1M+"]
Z = []
count = 0

for r in ranges:
  z = []
  for state in states:
    X.append(state.get('key'))
    z.append(state['reverse']['fund_amt']['buckets'][r]['doc_count'])
  Z.append(z)



app = dash.Dash()
app.css.append_css({
    "external_url": r'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css'
})
app.scripts.append_script({
    "external_url": r'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js'
})

app.layout = Div(
  className='row',
  style={"margin-top":"50px"},
  children=[
    Div(
      className='col s12 z-depth-2',
      children=[
        Div(
          id='heat-map-div',
          className='row',
          style = {'margin':'10px'},
          children=[
            Graph(
              id ='heat-map',
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
                    colorbar={'thickness':15,'x':1.01, 'xpad':0, 'ypad':0,}
                  )
                ],
                'layout': 
                  go.Layout(
                    # title = 'Funding by State',
                    xaxis={'title': 'States'},
                    yaxis={'title': 'Funding (Dollar Amount)','tickprefix':"  "},
                    margin={'l':110,'r':40,'t':30,'b':50,},
                  )
              },
              config={
                'displayModeBar': False
              }
            )
          ]
        )
      ]
    ),
    Div(
      className='col s6'
    ),
    Div(
      className='col s6'
    )
  ]
)



if __name__ == '__main__':
    app.run_server(debug=True)

#     data = [
#   dict(
#     type='choropleth',
#     autocolorscale = True,
#     locations = states, 
#     z = rtg, 
#     locationmode = 'USA-states',
#     marker = dict(line = dict(color = 'rgb(255,255,255)',width = 2)),
#     colorbar = dict(title = "Deck Condition Ratings")
#   )
# ]


# data = [dict(type='choropleth',autocolorscale = True,
#         locations = states, z = rtg, locationmode = 'USA-states',
#         marker = dict(line = dict(color = 'rgb(255,255,255)',width = 2)),
#         colorbar = dict(title = "Deck Condition Ratings"))]

# layout = dict(
#         title = 'Deck Condition Ratings for Sample Dataset',
#         geo = dict(
#             scope='usa',
#             projection=dict( type='albers usa' ),
#             showlakes = True,
#             lakecolor = 'rgb(255, 255, 255)'),
#              )
    
# fig = dict( data=data, layout=layout )
# plotly.plotly.iplot(fig, filename='cloropleth-map' )
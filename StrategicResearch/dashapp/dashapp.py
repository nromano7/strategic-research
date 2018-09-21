# -*- coding: utf-8 -*-
import dash
from dash_core_components import Graph, Input, Dropdown
from dash_html_components import Div, H1, H2, H3, H4, H5, H6, P, A, Span, Big, Main, Button
import plotly.graph_objs as go
import dashapp.app.figures as figs
import dashapp.app.aggregations as aggs
from flaskapp import app as flaskapp

# external css and js
external_stylesheets = [
  "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
  "https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0/css/bootstrap.min.css",
  "https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.5.4/css/mdb.min.css"
]
external_scripts = [
  "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js",
  "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.13.0/umd/popper.min.js",
  "https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.0.0/js/bootstrap.min.js",
  "https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.5.4/js/mdb.min.js"
]

# initialize dash app
app = dash.Dash(__name__, 
                server=flaskapp, 
                url_base_pathname='/dashboard',
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)

# data = aggs.ProjectCountByState(selection)
# figure = figs.ProjectCountMap2(data)

app.layout =  (
  Div(
    id="",
    className="",
    style="",
    children=[
      # ///// MAP /////
      # Graph(
      #   id='project-count-map',
      #   style={"height":"100%","overflow": "hidden"},
      #   figure=figs.ProjectCountMap2(data),
      #   config={'displayModeBar': False},
      # )
    ]
  )
)


application = app.server
if __name__ == '__main__':
    application.run(debug=True)
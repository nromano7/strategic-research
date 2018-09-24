# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc #import Graph, Input, Dropdown
import dash_html_components as html#import Div, H1, H2, H3, H4, H5, H6, P, A, Span, Big, Main, Button
import plotly.graph_objs as go
import dashapp.figure as figure
import dashapp.aggregate as aggregate
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

mapbox_access_token = r"pk.eyJ1IjoibnJvbWFubzciLCJhIjoiY2ppa2prYjQ2MWszczNsbnh5YnhkZTh1aSJ9.5qBV5E8g3oxlo3ZFL4n6Zw"

# initialize dash app
app = dash.Dash(__name__, 
                server=flaskapp, 
                url_base_pathname='/dashboard',
                external_scripts=external_scripts,
                external_stylesheets=external_stylesheets)

app.layout = html.Div(
  className="dash-grid-container grey lighten-3",
  children=[
    html.Div(
      id="filter-panel",
      className="card card-body z-depth-1 pt-2",
      children=[
        html.H4("Filter results by element or LTBP research topics."),
        html.Div(
          className="row",
          children=[
            html.Div(
              className="col text-center",
              children=[
                # html.H5("Record Set"),
                dcc.Dropdown(
                  id="record_set_selection",
                  className="text-left",
                  options=[
                    dict(label="All Bridges & Structures", value="all"),
                    dict(label="Bridges: All Elements", value="bridges"),
                    dict(label="Untreated Decks", value="untreated_decks"),
                    dict(label="Treated Decks", value="treated_decks"),
                    dict(label="Joints", value="joints"),
                    dict(label="Bearings", value="bearings"),
                    dict(label="Coatings", value="coatings")
                  ],
                  placeholder="Select bridge element...",
                  value="",
                  searchable=False,
                  clearable=False
                )
              ]
            ),
            html.Div(
              className="col text-center",
              children=[
                # html.H5("LTBP Research Topics"),
                dcc.Dropdown(
                  id="tags-selection",
                  className="text-left",
                  options=[
                    dict(label="All", value="all"),
                    dict(label="Construction Quality", value="construction_quality"),
                    dict(label="Design & Details", value="design_and_details"),
                    dict(label="Material Specifications", value="material_specifications"),
                    dict(label="Live Load", value="live_load"),
                    dict(label="Environment", value="environment"),
                    dict(label="Structural Integrity", value="structural_integrity"),
                    dict(label="Structural Condition", value="structural_condition"),
                    dict(label="Functionality", value="functionality"),
                    dict(label="Cost", value="cost")
                  ],
                  placeholder="Select LTBP research topic...",
                  value="",
                  searchable=False,
                  clearable=False
                )
              ]
            )
          ]
        )
      ]
    ),
    html.Div(
      id="projects-panel",
      className="card card-body text-center justify-content-center z-depth-1 p-1",
      children=[
        html.H2("{:,d}".format(aggregate.project_count()['total'])),
        html.H3("Projects", className="text-muted")
      ]
    ),
    # html.Div(
    #   id="active-projects-panel",
    #   className="card card-body text-center justify-content-center z-depth-1 p-1",
    #   children=[
    #     html.H3("{:,d}".format(aggregate.project_count()['active']), className="mb-0"),
    #     html.P(html.Small("Active"), className="text-muted mb-0")
    #   ]
    # ),
    # html.Div(
    #   id="programmed-projects-panel",
    #   className="card card-body text-center justify-content-center z-depth-1 p-1",
    #   children=[
    #    html.H3("{:,d}".format(aggregate.project_count()['programmed']), className="mb-0"),
    #   html.P(html.Small("Programmed"), className="text-muted mb-0")
    #   ]
    # ),
    # html.Div(
    #   id="proposed-projects-panel",
    #   className="card card-body text-center justify-content-center z-depth-1 p-1",
    #   children=[
    #     html.H3("{:,d}".format(aggregate.project_count()['proposed']), className="mb-0"),
    #     html.P(html.Small("Proposed"), className="text-muted mb-0")
    #   ]
    # ),
    # html.Div(
    #   id="complete-projects-panel",
    #   className="card card-body text-center justify-content-center z-depth-1 p-1",
    #   children=[
    #     html.H3("{:,d}".format(aggregate.project_count()['completed']), className="mb-0"),
    #     html.P(html.Small("Complete"), className="text-muted mb-0")
    #   ]
    # ),
    html.Div(
      id="publications-panel",
      className="card card-body text-center justify-content-center z-depth-1 p-1",
      children=[
        html.H2("{:,d}".format(aggregate.publication_count())),
        html.H3("Publications", className="text-muted")
      ]
    ),
    dcc.Graph(
      id='project-count-map',
      className="z-depth-1",
      figure=figure.project_count_map(),
      config={'displayModeBar': False}
    ),
    dcc.Graph(
      id='funding-heatmap',
      className="z-depth-1",
      figure=figure.funding_heatmap(),
      config={'displayModeBar': False}
    ),
    dcc.Graph(
      id='barchart1',
      className="z-depth-1",
      figure=figure.bar_chart("attributes"),
      config={'displayModeBar': False}
    ),
    dcc.Graph(
      id='barchart2',
      className="z-depth-1",
      figure=figure.bar_chart("inputs"),
      config={'displayModeBar': False}
    ),
    dcc.Graph(
      id='barchart3',
      className="z-depth-1",
      figure=figure.bar_chart("performance"),
      config={'displayModeBar': False}
    ),
    html.H4("Attributes",id="barchart1-heading",className="p-2 text-left h-25"),
    html.H4("Inputs",id="barchart2-heading",className="p-2 text-left h-25"),
    html.H4("Performance",id="barchart3-heading",className="p-2 text-left h-25"),
    html.H4("Count by State",id="project-count-map-heading",className="p-2 text-left"),
    html.H4("Funding by State",id="funding-heatmap-heading",className="p-2 text-left")
  ]
)

@app.callback(dash.dependencies.Output('projects-panel','children'),[dash.dependencies.Input('tags-selection','value')])
def updateTotalProjectCount(selection):
  children=[
    html.H2("{:,d}".format(aggregate.project_count(selection)['total'])),
    html.H3("Projects", className="text-muted")
  ]
  return children

@app.callback(dash.dependencies.Output('publications-panel','children'),[dash.dependencies.Input('tags-selection','value')])
def updateTotalPublicationCount(selection):
  children=[
    html.H2("{:,d}".format(aggregate.publication_count(selection))),
    html.H3("Publications", className="text-muted")
  ]
  return children

@app.callback(dash.dependencies.Output('project-count-map','figure'),[dash.dependencies.Input('tags-selection','value')])
def updateProjectCountMap(selection):
  data = aggregate.project_count_by_state(selection)
  return_figure = figure.project_count_map(data)
  return return_figure


application = app.server
if __name__ == '__main__':
    application.run(debug=True)
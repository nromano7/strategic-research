import dash
from dash_core_components import Graph, Input, Dropdown
from dash_html_components import Div, H1, H2, H3, H4, H5, H6, P, A, Span, Big, Main, Button
import plotly.graph_objs as go

import app.figures as figs
import app.aggregations as aggs

app = dash.Dash(__name__)
application = app.server

# materialize css
app.css.append_css({
    "external_url": r'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css'
})
# materialize js
app.scripts.append_script({
    "external_url": r'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js'
})
# loading screen css
app.css.append_css({"external_url": r"https://codepen.io/chriddyp/pen/brPBPO.css"})

app.title = 'Strategic Research'

z_depth = 'z-depth-4'

app.layout =  (
  # ///// START MAIN /////
  Div(
    id="main",
    className="",
    style={"background-color":"#eeeeee"},
    children=[

      # ///// START CONTENT /////
      Div(
        id="content",
        className="",
        style={"padding":"20px 100px 20px 100px"},
        children=[

          # ///// START ROW 1 /////
          Div(
            id="row1",
            className="",
            style={},
            children=[

              Div(
                id="",
                className='row',
                style={"display":"flex"},
                children=[

                  # ///// SEARCH BAR /////
                  Div(
                    id="",
                    className="col s6",
                    style={},
                    children=[

                      Div(
                        id="search-bar",
                        className=f"blue-grey lighten-1 white-text {z_depth}",
                        style={'padding':'10px',"height":"100%"},
                        children=[

                          P(
                            id="",
                            style={"margin":"0px","font-size":"18px"},
                            children=[
                              "Search by subject area or research topic (e.g. freeze-thaw, deterioation modeling, etc.)."
                            ]
                          ),

                          Div(className="divider"),

                          Div(
                            id="",
                            className="valign-wrapper",
                            style={},
                            children=[

                              Div(
                                id="",
                                className="col s10",
                                style={},
                                children=[

                                  Input(
                                    id="search",
                                    className="white-text",
                                    style={"font-size":"20px","margin-top":"10px"},
                                    type="text",
                                    value="",
                                  ),
                                  
                                ]
                              ),

                              Div(
                                id="",
                                className="col s2 center-align",
                                style={},
                                children=[

                                  Button(
                                    "Search",
                                    id="search-btn",
                                    className="waves-effect waves-light btn blue darken-2"
                                  )
                                ]
                              )
                            ]
                          )
                        ]
                      )
                    ]
                  ),

                  # ///// DROPDOWN MENU /////
                  Div(
                    id="",
                    className="col s6",
                    style={},
                    children=[

                      Div(
                        id="dropdown-menu",
                        className=f"blue-grey lighten-1 white-text {z_depth}",
                        style={"background-color":"#ffffff","padding":"10px"},
                        children=[

                          P(
                            children=['Filter by bridge element, inputs/attributes, or performance metric.'],
                            style={'margin':'0px',"font-size":"18px"}
                          ),

                          Div(
                            className='divider'
                          ),

                          Div(
                            id="menu-row",
                            className="row black-text",
                            style={"margin":"0px","padding":"15px 0px 10px 0px"},
                            children=[

                               Div(
                                id="",
                                className="col s4",
                                style={},
                                children=[

                                  Dropdown(
                                    id="dropdown-1",
                                    options=[
                                      dict(label="Elements", value=""),
                                      dict(label="Untreated Decks", value="UTdecks"),
                                      dict(label="Treated Decks", value="Tdecks"),
                                      dict(label="Joints", value="joints"),
                                      dict(label="Coatings", value="coatings")
                                    ],
                                    value="",
                                    searchable=False
                                  )
                                ]
                              ),

                              Div(
                                id="",
                                className="col s4",
                                style={},
                                children=[

                                  Dropdown(
                                    id='dropdown-2',
                                    options=[
                                      dict(label="Inputs/Attributes", value=""),
                                      dict(label="Construction", value="construction"),
                                      dict(label="Design", value="design"),
                                      dict(label="Environment", value="environment"),
                                      dict(label=r"Maintenance & Preservation", value="maintenance"),
                                      dict(label="Materials", value="materials"),
                                    ],
                                    value="",
                                    searchable=False
                                  )
                                ]
                              ),

                              Div(
                                id="",
                                className="col s4",
                                style={},
                                children=[

                                  Dropdown(
                                    id='dropdown-3',
                                    options=[
                                      dict(label="Performance", value=""),
                                      dict(label="Cost", value="cost"),
                                      dict(label="Functionality", value="functionality"),
                                      dict(label="Structural Condition", value="condition"),
                                      dict(label="Structural Integrity", value="integrity")
                                    ],
                                    value="",
                                    searchable=False
                                  )
                                ]
                              )
                            ]
                          )
                        ]
                      )
                    ]
                  )
                ]
              )
            ]
          ),
          # ///// END ROW 1 /////

          # ///// START ROW 2 /////
          Div(
            id="row2",
            className="",
            style={},
            children=[

              Div(
                id="",
                className="row",
                style={"display":"flex"},
                children=[

                  # ///// START LEFT PANEL /////
                  Div(
                    id="left-panel",
                    className="col s6",
                    style={},
                    children=[

                      Div(
                        id="",
                        className=f"{z_depth}",
                        style={"height":"100%"},
                        children=[

                          # ///// MAP /////
                          Graph(
                            id='project-count-map',
                            style={"height":"100%"},
                            figure=figs.ProjectCountMap2(),
                            config={'displayModeBar': False},
                          )
                        ]
                      )
                    ]
                  ),
                  # ///// END LEFT PANEL /////

                  # ///// START RIGHT PANEL 1 /////
                  Div(
                    id="right-panel-1",
                    className="col s2",
                    style={},
                    children=[
                      
                      # ///// PROJECT STATS CARD /////
                      Div(
                        id="project-stats-card",
                        className=f"card blue-grey {z_depth}",
                        # style={"margin-top": "0px"},
                        children=[

                          Div(
                            id="project-count-div",
                            className="card-content white-text center-align",
                            style={},
                            children=[

                              H1(
                                id="project-count",
                                className="",
                                style={"margin":"0px"},
                                children=[
                                  "{:,d}".format(aggs.ProjectCount()['total'])
                                ]
                              ),

                              H6("Total Projects",style={"margin":"5px 0px 10px 0px"}),

                              Div(
                                id="",
                                className="divider",
                                style={"margin":"20px 0px 20px 0px"},
                              ),

                              Div(
                                id="project-status-div",
                                className="row",
                                style={"margin":"5px 20px 5px 10px"},
                                children=[

                                  Div(
                                    id="",
                                    className="col s6",
                                    style={},
                                    children=[

                                      Div(
                                        id="stauses",
                                        className="card-stacked left-align",
                                        style={},
                                        children=[
                                          P("Active"),
                                          P("Programmed"),
                                          P("Proposed")
                                        ]
                                      )
                                    ]
                                  ),

                                  Div(
                                    id="",
                                    className="col s6",
                                    style={},
                                    children=[

                                      Div(
                                        id="status-count",
                                        className="card-stacked right-align",
                                        style={},
                                        children=[
                                          P("{:,d}".format(aggs.ProjectCount()['active'])),
                                          P("{:,d}".format(aggs.ProjectCount()['programmed'])),
                                          P("{:,d}".format(aggs.ProjectCount()['proposed']))
                                        ]
                                      )
                                    ]
                                  )
                                ]
                              )
                            ]
                          ),

                          Div(
                            id="project-nav",
                            className="card-action center-align",
                            style={},
                            children=[

                              A(
                                id="project-results",
                                style={"margin":"0px"},
                                href="#",
                                children=[
                                  "View Projects"
                                ]
                              )
                            ]
                          )
                        ]
                      ),
                      
                      # ///// PUBLICATION STATS CARD /////
                      Div(
                        id="publication-stats-card",
                        className=f"card blue-grey {z_depth}",
                        style={"margin":"1rem 0 .5rem 0"},
                        children=[

                          Div(
                            id="publications-count-div",
                            className="card-content white-text center-align",
                            style={},
                            children=[

                              H1(
                                id='publication-count',
                                className="",
                                style={"margin":"0px"},
                                children=[
                                  "{:,d}".format(aggs.PublicationCount())
                                ]
                              ),

                              H6("Total Publications",style={"margin":"5px 0px 10px 0px"})
                            ]
                          ),

                          Div(
                            id="publication-nav",
                            className="card-action center-align",
                            style={},
                            children=[

                              A(
                                id="publication-results",
                                style={"margin":"0px"},
                                href="#",
                                children=[
                                  "View Publications"
                                ]
                              )
                            ]
                          )
                        ]
                      )
                    ]
                  ),
                  # ///// END RIGHT PANEL 1 /////
                  
                  # ///// START RIGHT PANEL 2 /////
                  Div(
                    id="right-panel-2",
                    className="col s4",
                    style={},
                    children=[
                      
                      Div(
                        id="",
                        className=f"card {z_depth}",
                        style={"margin-top":"0px","height":"100%"},
                        children=[

                          # ///// TERMS BAR CHART /////
                          Div(
                            id="",
                            className="card-content",
                            style={"padding":"15px"},
                            children=[
                              
                              Span(
                                id="",
                                className="card-title",
                                style={},
                                children=[
                                  "Projects in the LTBP Framework"
                                ]
                              ),

                              Div(className="divider"),

                              Graph(
                                id='bar-chart',
                                className="",
                                style={},
                                figure=figs.TermsBarChart(),
                                config={'displayModeBar': False}
                              )
                            ]
                          )
                        ]
                      )
                    ]
                  )
                  # ///// END RIGHT PANEL 2 /////
                ]
              )
            ]
          ),
          # ///// END ROW 2 /////

          # ///// START ROW 3 /////
          Div(
            id="row3",
            className="",
            style={},
            children=[

              Div(
                id="",
                className="row",
                style={},
                children=[

                  Div(
                    id="",
                    className="col s12",
                    style={},
                    children=[

                      Div(
                        id="",
                        className=f"card {z_depth}",
                        style={"margin-top":"0px","height":"100%"},
                        children=[

                          Div(
                            id="",
                            className="card-content",
                            style={"padding":"15px"},
                            children=[
                              
                              Span(
                                id="",
                                className="card-title",
                                style={},
                                children=[
                                  "Discover project funding by state and amount..."
                                ]
                              ),

                              Div(className="divider"),

                              Graph(
                                id ='FundingLevelHeatMap-heatmap',
                                figure = figs.FundingLevelHeatMap(),
                                config={'displayModeBar': False}
                              )
                            ]
                          )
                        ]
                      )
                    ],
                  ),
                ],
              ),
            ],
          ),
          # ///// END ROW 3 /////

          # ///// START ROw 4 /////
          Div(
            id="row4",
            className="",
            style={},
            children=[

              Div(
                id="",
                className="row",
                style={},
                children=[

                  Div(
                    id="",
                    className="col s6",
                    style={},
                    children=[

                      Div(
                        id="",
                        className=f"{z_depth}",
                        children=[

                          Graph(
                            id ='FundingByYear-histogram',
                            figure = figs.FundingByYearHistogram(),
                            config={'displayModeBar': False}
                          )
                        ]
                      )
                    ],
                  ),

                  Div(
                    id="",
                    className="col s6",
                    style={},
                    children=[

                      Div(
                        id="",
                        className=f"{z_depth}",
                        children=[

                          Graph(
                            id ='project-count-histogram',
                            figure = figs.ProjectCountByYearHistogram(),
                            config={'displayModeBar': False}
                          )
                        ]
                      )
                    ],
                  ),
                ],
              ),
            ],
          )
          # ///// END ROW 4 /////
        ]
      )
    ]
  )
)

@app.callback(dash.dependencies.Output('project-count','children'),[dash.dependencies.Input('dropdown-2','value')])
def updateTotalProjectCount(selection):
  response = "{:,d}".format(aggs.ProjectCount(selection)['total'])
  return response

@app.callback(dash.dependencies.Output('publication-count','children'),[dash.dependencies.Input('dropdown-2','value')])
def updatePublicationCount(selection):
  response = "{:,d}".format(aggs.PublicationCount(selection))
  return response

@app.callback(dash.dependencies.Output('status-count','children'),[dash.dependencies.Input('dropdown-2','value')])
def updateActiveProjectCount(selection):
  children = [
    P("{:,d}".format(aggs.ProjectCount(selection)['active'])),
    P("{:,d}".format(aggs.ProjectCount(selection)['programmed'])),
    P("{:,d}".format(aggs.ProjectCount(selection)['proposed']))
  ]
  return children

@app.callback(dash.dependencies.Output('project-count-map','figure'),[dash.dependencies.Input('dropdown-2','value')])
def updateProjectCountMap(selection):
  data = aggs.ProjectCountByState(selection)
  figure = figs.ProjectCountMap2(data)
  return figure

@app.callback(dash.dependencies.Output("FundingLevelHeatMap-heatmap","figure"),[dash.dependencies.Input("dropdown-2","value")])
def updateFundingHeatMap(selection):
  data = aggs.FundingLevelByState(selection)
  figure = figs.FundingLevelHeatMap(data)
  return figure

@app.callback(dash.dependencies.Output('FundingByYear-histogram','figure'),[dash.dependencies.Input('dropdown-2','value')])
def updateFundingByYearHistogram(selection):
  data = aggs.FundingByYear(selection)
  figure = figs.FundingByYearHistogram(data)
  return figure

@app.callback(dash.dependencies.Output('project-count-histogram','figure'),[dash.dependencies.Input('dropdown-2','value')])
def updateProjectCountByYearHistogram(selection):
  data = aggs.ProjectCountByYear(selection)
  figure = figs.ProjectCountByYearHistogram(data)
  return figure


if __name__ == '__main__':
    application.run(debug=True)
import sys
import os
sys.path.append(os.getcwd())

import dash
from dash_core_components import Graph, Input, Dropdown
from dash_html_components import Div, H1, H2, H3, P, Span, Big
from figures import figs
from aggregations import aggs
import plotly.graph_objs as go

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
# Loading screen CSS
app.css.append_css({"external_url": r"https://codepen.io/mikesmith1611/pen/QOKgpG"})

app.title = 'Strategic Research'

z_depth = 'z-depth-1'

app.layout = Div(
  children=[
    Div(
      children=[
        Div(
          children=[
            Div(
              children=[
                Div(
                  children = [
                    Div(
                      children=[
                        Input(
                          placeholder='Search...',
                          type='text',
                          value='',
                          # style={'margin':'0px 10px 10px 10px'},
                        )
                      ],
                      # style={'margin-right':'20px'},
                    )
                  ],
                  className=f'{z_depth}',
                )
              ],
              className="col s6",
              id='search-bar',
              # style={'padding-left':'0px'},
            ),
            Div(
              children=[
                Div(
                  children=[
                    Div(
                      children = [
                        Dropdown(
                          id='dropdown-1',
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
                      ],
                      # style={'margin':'0px',"padding":"0px"},
                    )
                  ],
                  className="col s4",
                  # style={'margin':'10px',"padding":"0px"},
                ),
                Div(
                  children=[
                    Div(
                      children = [
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
                      ],
                      # style={'margin':'0px',"padding":"0px"},
                    )
                  ],
                  className="col s4",
                  # style={'margin':'10px',"padding":"0px"},
                ),
                Div(
                  children=[
                    Div(
                      children = [
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
                      ],
                      # style={'margin':'0px',"padding":"0px"},
                    )
                  ],
                  className="col s4",
                  # style={'margin':'10px',"padding":"0px"},
                )
              ],
              className="col s6 left-align z-depth-2 valign-wrapper",
              id='dropdowns',
              # style={'padding':'0px',"margin":"0px"},
            )
          ],
          className='row valign-wrapper',
          id='row1',
        ),
        Div(
          children=[
            Div(
              children=[
                Div(
                  children=[
                    Graph(
                      id='project-count-map',
                      figure=figs.ProjectCountMap2(),
                      config={'displayModeBar': False},
                      # style={"pagging":"0px"}
                    )
                  ],
                  className= f'{z_depth}',
                  id='chloropleth-map-div',
                  
                )
              ],
              className='col s6',
              id='row2-col-s6',
              # style={'padding-left':'0px'},
            ),
            Div(
              children=[
                Div(
                  children=[
                    Div(
                      children=[
                        Div(
                          children=[
                            H1(
                              children=[
                                "{:,d}".format(aggs.ProjectCount()['total'])
                              ],
                              # style={"margin-top":"0px","margin-bottom":"8px",},
                              id='total-project-count'
                            ),
                            P(
                              'Total Projects'
                            )
                          ],
                          className="card-content white-text center-align",
                          id='project-stats-card-text',
                          # style={"padding":"18px","min-width":"185px"},
                        ),
                        Div(
                          children=[
                            Div(
                              children=[
                                Div(
                                  children=[
                                    Big(
                                      children=[
                                        Big(
                                          children=[
                                            Span('Active:\t',
                                            style=dict(margin="0px")
                                            ),
                                          ]
                                        )
                                      ]
                                    ),
                                    Big(
                                      children=[
                                        Span(
                                          children=[
                                            "{:,d}".format(aggs.ProjectCount()['active'])
                                          ],
                                          id='active-project-count'
                                        )
                                      ]
                                    )
                                  ]
                                ),
                                Div(
                                  children=[
                                    Big(
                                      children=[
                                        Big(
                                          children=[
                                            Span('Programmed:\t',
                                              style=dict(margin="0px")
                                            ),
                                          ]
                                        )
                                      ]
                                    ),
                                    Big(
                                      children=[
                                        Span(
                                          children=[
                                            "{:,d}".format(aggs.ProjectCount()['programmed'])
                                          ],
                                          id='programmed-project-count'
                                        )
                                      ]
                                    )
                                  ]
                                ),
                                Div(
                                  children=[
                                    Big(
                                      children=[
                                        Big(
                                          children=[
                                            Span('Proposed:\t',
                                              # style=dict(margin="0px")
                                            ),
                                          ]
                                        )
                                      ]
                                    ),
                                    Big(
                                      children=[
                                        Span(
                                          children=[
                                            "{:,d}".format(aggs.ProjectCount()['proposed'])
                                          ],
                                          id='proposed-project-count'
                                        )
                                      ]
                                    )
                                  ]
                                )                            
                              ],
                              className="card-content white-text",
                              # style={"padding":"18px"},
                            )
                          ],
                          className="card-stacked",
                        )
                      ],
                      className='card horizontal blue-grey z-depth-2',
                      id='project-stats-card',
                      # style={"margin":"0px"},
                    ),
                    Div(
                      children=[
                        Div(
                          children=[
                            H1(
                              children=[
                                "{:,d}".format(aggs.PublicationCount())
                              ],
                              # style={"margin-top":"0px","margin-bottom":"8px",},
                              id='publication-count'
                            ),
                            P(
                              'Total Publications'
                            )
                          ],
                          className="card-content white-text center-align",
                          id='publication-stats-card-text',
                        )
                      ],
                      className='card blue-grey z-depth-2',
                      id='publication-stats-card',
                    )
                  ],
                  id='stats-div',
                  # style={"width":"95%"},
                )
              ],
              className='col s3',
              id='row2-col-s3',
              # style={'padding-right':'0px',"margin":"0px"},
            ),
            Div(
              children=[
                Div(
                  children=[
                    Graph(
                      id='pie-chart',
                      figure=figs.TermsPieChart(),
                      config={'displayModeBar': False}
                    )
                  ],
                  style={"margin":"10px"},
                )
              ],
              className='col s3 z-depth-2',
              # style={"margin-left":"0px","padding":"0px"},
              id='piechart-div',
            )
          ],
          className='row',
          id='row2',
        ),
        Div(
          children=[
            Div(
              children=[
                Graph(
                  id ='FundingLevelHeatMap-heatmap',
                  figure = figs.FundingLevelHeatMap(),
                  config={'displayModeBar': False}
                )
              ],
              className='col s12 z-depth-2',
              id='FundingLevelHeatMap-heatmap-div',
              # style={"padding":"10px"}
            )
          ],
          className='row',
          id='row3',
        ),
        Div(
          children=[
            Div(
              children=[
                Graph(
                  id ='FundingByYear-histogram',
                  figure = figs.FundingByYearHistogram(),
                  config={'displayModeBar': False}
                )
              ],
              className='col s6 z-depth-2',
              id='FundingByYear-histogram-div',
              # style={"padding":"10px"},
            ),
            Div(
              children=[
                Graph(
                  id ='project-count-histogram',
                  figure = figs.ProjectCountByYearHistogram(),
                  config={'displayModeBar': False}
                )
              ],
              className='col s6 z-depth-2',
              id='project-count-histogram-div',
              # style={"padding":"10px"},
            )
          ],
          className='row',
          id='row4',
        )    
      ],
      className='row',
      # style={"padding":"20px 100px 20px 100px"},
    )
  ],
  style={"background-color":"#eeeeee"}
)

@app.callback(dash.dependencies.Output('project-count-map','figure'),[dash.dependencies.Input('dropdown-2','value')])
def updateProjectCountMap(selection):
  data = aggs.ProjectCountByState(selection)
  figure = figs.ProjectCountMap2(data)
  return figure

@app.callback(dash.dependencies.Output('total-project-count','children'),[dash.dependencies.Input('dropdown-2','value')])
def updateTotalProjectCount(selection):
  response = "{:,d}".format(aggs.ProjectCount(selection)['total'])
  return response

@app.callback(dash.dependencies.Output('publication-count','children'),[dash.dependencies.Input('dropdown-2','value')])
def updatePublicationCount(selection):
  response = "{:,d}".format(aggs.PublicationCount(selection))
  return response

@app.callback(dash.dependencies.Output('active-project-count','children'),[dash.dependencies.Input('dropdown-2','value')])
def updateActiveProjectCount(selection):
  response = "{:,d}".format(aggs.ProjectCount(selection)['active'])
  return response

@app.callback(dash.dependencies.Output('programmed-project-count','children'),[dash.dependencies.Input('dropdown-2','value')])
def updateProgrammedProjectCount(selection):
  response = "{:,d}".format(aggs.ProjectCount(selection)['programmed'])
  return response

@app.callback(dash.dependencies.Output('proposed-project-count','children'),[dash.dependencies.Input('dropdown-2','value')])
def updateProposedProjectCount(selection):
  response = "{:,d}".format(aggs.ProjectCount(selection)['proposed'])
  return response

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
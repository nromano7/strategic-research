import sys
import os
sys.path.append(os.getcwd())

import dash
from dash_core_components import Graph, Input
from dash_html_components import Div, H1, H2, H3, P, Span, Big
from figures import figs
from aggregations import aggs
import plotly.graph_objs as go

app = dash.Dash()
app.css.append_css({
    "external_url": r'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/css/materialize.min.css'
})
app.scripts.append_script({
    "external_url": r'https://cdnjs.cloudflare.com/ajax/libs/materialize/1.0.0-beta/js/materialize.min.js'
})
# Loading screen CSS
app.css.append_css({"external_url": r"https://codepen.io/mikesmith1611/pen/QOKgpG"})

app.title = 'Strategic Research'

app.layout = Div(
  className='row',
  id='body',
  style={"margin-top":"20px", "margin-left":"100px","margin-right":"100px"},
  children=[
    Div(
      className='row',
      id='row1',
      children=[
        Div(
          className="col6",
          children=[
            Div(
              className='col s6 z-depth-2',
              id='search-bar',
              children = [
                Input(
                  placeholder='Search...',
                  type='text',
                  value=''
                )
              ]
            )
          ]
        ),
        Div(
          className="col6",
          children=[
            Div(
              className='col s6 z-depth-2',
              id='search-bar2',
              children = [
                Input(
                  placeholder='Search...',
                  type='text',
                  value=''
                )
              ]
            )
          ]
        )
      ]
    ),
    Div(
      className='row',
      id='row2',
      children=[
        Div(
          className='col s6',
          id='row2-col-s6',
          style={'padding-left':'0px'},
          children=[
            Div(
              className= 'z-depth-2',
              id='chloropleth-map-div',
              children=[
                Graph(
                  id='chloropleth-map',
                  figure=figs.ProjectCountMap2(),
                  config={'displayModeBar': False}
                )
              ]
            )
          ]
        ),
        Div(
          className='col s3',
          id='row2-col-s3',
          style={'padding-right':'0px',"margin":"0px"},
          children=[
            Div(
              id='stats-div',
              children=[
                Div(
                  className='card horizontal blue-grey z-depth-2',
                  id='project-stats-card',
                  style={"margin":"0px"},
                  children=[
                    Div(
                      className="card-content white-text center-align",
                      id='project-stats-card-text',
                      style={"padding-left":"36px"},
                      children=[
                        H1("{:,d}".format(aggs.ProjectCount()['total']),
                          style={"margin-top":"0px","margin-bottom":"8px",}
                        ),
                        P(
                          'Total Projects'
                        )
                      ]
                    ),
                    Div(
                      className="card-stacked",
                      children=[
                        Div(
                          className="card-content white-text",
                          children=[
                            # Div(
                            #   children=[
                            #     Big(
                            #       children=[
                            #         Big(
                            #           Span('Complete:\t',
                            #           style=dict(margin="0px")
                            #           ),
                            #         )
                            #       ]
                            #     ),
                            #     Big(Span("{:,d}".format(aggs.ProjectCount()['complete'])))
                            #   ]
                            # ),
                            Div(
                              children=[
                                Big(
                                  children=[
                                    Big(
                                      Span('Active:\t',
                                      style=dict(margin="0px")
                                      ),
                                    )
                                  ]
                                ),
                                Big(Span("{:,d}".format(aggs.ProjectCount()['active'])))
                              ]
                            ),
                            Div(
                              children=[
                                Big(
                                  children=[
                                    Big(
                                      Span('Programmed:\t',
                                      style=dict(margin="0px")
                                      ),
                                    )
                                  ]
                                ),
                                Big(Span("{:,d}".format(aggs.ProjectCount()['programmed'])))
                              ]
                            ),
                            Div(
                              children=[
                                Big(
                                  children=[
                                    Big(
                                      Span('Proposed:\t',
                                      style=dict(margin="0px")
                                      ),
                                    )
                                  ]
                                ),
                                Big(Span("{:,d}".format(aggs.ProjectCount()['proposed'])))
                              ]
                            )                            
                          ]
                        )
                      ]
                    )
                  ]
                ),
                Div(
                  className='card blue-grey z-depth-2',
                  id='publication-stats-card',
                  children=[
                    Div(
                      className="card-content white-text center-align",
                      id='publication-stats-card-text',
                      # style={"padding-left":"36px"},
                      children=[
                        H1("{:,d}".format(aggs.PublicationCount()),
                          style={"margin-top":"0px","margin-bottom":"8px",}
                        ),
                        P(
                          'Total Publications'
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
    Div(
      className='row',
      id='row3',
      children=[
        Div(
          className='col s12 z-depth-2',
          id='FundingLevelHeatMap-heatmap-div',
          children=[
            Graph(
              id ='FundingLevelHeatMap-heatmap',
              figure = figs.FundingLevelHeatMap(),
              config={'displayModeBar': False}
            )
          ]
        )
      ]
    ),
    Div(
      className='row',
      id='row4',
      children=[
        Div(
          className='col s6 z-depth-2',
          id='FundingByYear-histogram-div',
          children=[
            Graph(
              id ='FundingByYear-histogram',
              figure = figs.FundingByYearHistogram(),
              config={'displayModeBar': False}
            )
          ]
        ),
        Div(
          className='col s6 z-depth-2',
        )
      ]
    )    
  ]
)

if __name__ == '__main__':
    app.run_server(debug=True)
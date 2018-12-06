import dash
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://cdnjs.cloudflare.com/ajax/libs/mdbootstrap/4.5.4/css/mdb.min.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    className="btn-group",
    children=[
        html.Button('Button 1', id='button1', className="btn btn-mdb-color active"),
        html.Button('Button 2', id='button2', className="btn btn-mdb-color"),
        html.Button('Button 3', id='button3', className="btn btn-mdb-color"),
        dcc.RadioItems(
            options=[
                {'label': 'New York City', 'value': 'NYC'},
                {'label': 'Montréal', 'value': 'MTL'},
                {'label': 'San Francisco', 'value': 'SF'}
            ],
            value='MTL',
            className="custom-control custom-radio",
            inputClassName="custom-control-input",
            labelClassName="custom-control-label"

        )
    ]
)


@app.callback(
    dash.dependencies.Output('button1', 'className'),
    [dash.dependencies.Input('button2', 'n_clicks'),
    dash.dependencies.Input('button3', 'n_clicks')])
def update_output(btn1, btn2):
    if btn1 or btn2:
        return "btn btn-mdb-color"
    else:
        return "btn btn-mdb-color active"




@app.callback(
    dash.dependencies.Output('button2', 'className'),
    [dash.dependencies.Input('button1', 'n_clicks'),
    dash.dependencies.Input('button3', 'n_clicks')])
def update_output(btn1, btn2):
    if btn1 or btn2:
        return "btn btn-mdb-color"
    else:
        return "btn btn-mdb-color active"




@app.callback(
    dash.dependencies.Output('button3', 'className'),
    [dash.dependencies.Input('button2', 'n_clicks'),
    dash.dependencies.Input('button1', 'n_clicks')])
def update_output(btn1, btn2):
    if btn1 or btn2:
        return "btn btn-mdb-color"
    else:
        return "btn btn-mdb-color active"



if __name__ == '__main__':
    app.run_server(debug=True)
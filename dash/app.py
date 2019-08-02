import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from plots.show_funds import risk_list, fund_data_layout
from plots.efficirnt_frontier import efficient_frontier_data_layout

from init_optmizer import optimizer

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        dcc.Graph(id='show-funds'),
        html.Div([
            dcc.Slider(
                id='risk-slider',
                min=0,
                max=100,
                value=65,
                marks={
                    0: {'label': '0', 'style': {'color': '#77b0b1'}},
                    26: {'label': '26'},
                    37: {'label': '37'},
                    100: {'label': '100', 'style': {'color': '#f50'}}
                },
            ),
            html.Div(id='risk-text', style={'margin-top': 20})
        ]),
        dcc.Graph(id='efficient-frontier')
    ],
        style={
            'width': '45%',
            'display': 'inline-block'
        }
    ),
    html.Div(id='allocation', style={'display': 'none'})
])


@app.callback(
    [Output('show-funds', 'figure'),
     Output('risk-text', 'children')],
    [Input('risk-slider', 'value')]
)
def update_risk(risk_val):
    return fund_data_layout(risk_val), '您选择的风险值为: {}'.format(risk_val)


@app.callback(
    Output('efficient-frontier', 'figure'),
    [Input('show-funds', 'selectedData'),
     Input('show-funds', 'clickData')]
)
def update_select(selectedData, clickData):
    if selectedData is None and clickData is None:
        efficient_data = optimizer.efficient_frontier()
    else:
        selected_points = set(selectedData['points']) if selectedData is not None else set()
        click_points = set(clickData['points']) if clickData is not None else set()
        points = selected_points | click_points
        selected_fund_code = [p['code'] for p in points]
        efficient_data = optimizer.efficient_frontier(columns=selected_fund_code)
    return efficient_frontier_data_layout(efficient_data)


# @app.callback(
#     Output('efficient-frontier', 'figure'),
#     [Input('show-funds', 'clickData')]
# )
# def update_click(clickData):
#     pass


if __name__ == '__main__':
    app.run_server(debug=True)

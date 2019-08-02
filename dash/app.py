import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from plots.show_funds import risk_list, fund_data_layout

df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.Div([
        dcc.Graph(id='show-funds'),
        dcc.Slider(
            id='risk-slider',
            min=min(risk_list),
            max=max(risk_list),
            value=min(risk_list),
            marks={str(risk): str(risk) for risk in risk_list},
            step=None
        )
    ],
        style={
            'width': '45%',
        }
    ),
    html.Div([
        dcc.Graph(id='efficient-frontier')
    ],
        style={
            'width': '45%',
        }
    )
])


@app.callback(
    Output('show-funds', 'figure'),
    [Input('risk-slider', 'value')]
)
def update_funds(risk_val):
    return fund_data_layout(risk_val)


@app.callback(
    Output('click-data', 'children'),
    [Input('basic-interactions', 'clickData')]
)
def update_click():
    pass


@app.callback(
    Output('selected-data', 'children'),
    [Input('basic-interactions', 'selectedData')]
)
def update_select():
    pass


if __name__ == '__main__':
    app.run_server(debug=True)

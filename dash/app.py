import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from plots.show_funds import risk_list, fund_data_layout
from plots.efficirnt_frontier import efficient_frontier_data_layout


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
        dcc.Graph(id='efficient-frontier', figure=efficient_frontier_data_layout('all'))
    ],
        style={
            'width': '45%',
        }
    ),
    html.Div(id='allocation', style={'display': 'none'})
])


@app.callback(
    Output('show-funds', 'figure'),
    [Input('risk-slider', 'value')]
)
def update_funds(risk_val):
    return fund_data_layout(risk_val)


@app.callback(
    Output('allocation', 'children'),
    [Input('risk-slider', 'value'),
     Input('show-funds', 'clickData'),
     Input('show-funds', 'selectedData')]
)
def update_allocation(risk_val, clickData, selectedData):
    risk_val = risk_val / 10
    data = optimizer.optimize(fixed='volatility', value=risk_val)
    allocation = [(key, val) for key, val in data.items() if val > 0]
    print(allocation)
    return allocation


if __name__ == '__main__':
    app.run_server(debug=True)

import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from time import time
import pathlib

from plots.backtesting import get_performance

parse_date = lambda d: datetime.strptime(d, "%Y-%m-%d")
PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()

# tbl = pd.DataFrame({"Sharpe ratio": [1, 2],
#                     "Ann. return": ["5%", "4.1%"],
#                     "payoff": [1.2, 2.4],
#                     "Calmar ratio": [1, 2],
#                     "Sortino ratio": [1, 2],
#                     "Maxdd": [1, 2]}, index=["Optimal", "selected"])
# tbl = tbl.T

parse_info = lambda info: [info['performance'][k] for k in ['p_y_r', 'alpha', 'winrate']] + \
                          [info['risk/return profile'][k] for k in ['maxdd', 'sharpe', 'sortino']]


def generate_td(e):
    if isinstance(e, float):
        e = "{:.4f}".format(e)
    return html.Td(e)


def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th()] + [html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr(
            [generate_td(dataframe.index[i])] +
            [generate_td(dataframe.iloc[i][col]) for col in dataframe.columns
             ]) for i in range(min(len(dataframe), max_rows))]
    )


def construct_traces(code):
    df0 = pd.read_csv(DATA_PATH.joinpath("adjusted_net_value.csv"), parse_dates=["datetime"], index_col=0)
    upper = pd.read_csv(DATA_PATH.joinpath("yhat_upper_total.csv"))
    lower = pd.read_csv(DATA_PATH.joinpath("yhat_lower_total.csv"))
    df1 = pd.read_csv(DATA_PATH.joinpath("yhat_total.csv"), parse_dates=["datetime"])
    forecast_time = df1['datetime']
    df0 = df0.loc['2017-01-01':'2018-12-11']
    history = df0[code]
    last = history[-1:]
    trace0 = go.Scatter(x=df0.index, y=history,
                        line_color="blue", name="history")
    upper = go.Scatter(x=forecast_time, y=pd.concat((last, upper[code])),
                       line_color="rgba(255,127,14,0.4)"
                       , mode='lines', name="upper")
    trace1 = go.Scatter(x=forecast_time,
                        y=pd.concat((last, df1[code])),
                        line_color="rgba(255,127,14,1)", fill="tonexty",
                        mode='lines', name="forecast")
    lower = go.Scatter(x=forecast_time, y=pd.concat((last, lower[code])),
                       line_color="rgba(255,127,14,0.4)", fill="tonexty",
                       mode='lines', name="lower")
    return trace0, upper, trace1, lower


def get_stock_figdata(code):
    traces = construct_traces(code)
    fig_data = {

        'data': traces,
        "layout": {
            # "annotations": [
            #     go.layout.Annotation(
            #         x=1.2,
            #         y=-0.1,
            #         showarrow=False,
            #         text="Custom x-axis title",
            #         xref="paper",
            #         yref="paper"
            #     ),
            #     go.layout.Annotation(
            #         x=1.2,
            #         y=0.3,
            #         showarrow=False,
            #         text="Custom y-axis title",
            #         xref="paper",
            #         yref="paper"
            #     )
            # ],
            "legend": {'x': 0.9, 'y': 0.9},

            "title": {
                'text': "Stock Prices",
                'xanchor': 'center',
                'yanchor': 'bottom',
                'xref': 'paper'
            },
            "xaxis": {
                "type": "date",
                "title": "Date",
                "domain": [0, 1],
                "rangeslider": {
                    "visible": True
                },
                "rangeselector": {
                    "buttons": [
                        {
                            "step": "month",
                            "count": 1,
                            "label": "1 mo",
                            "stepmode": "backward"
                        },
                        {
                            "step": "month",
                            "count": 3,
                            "label": "3 mo",
                            "stepmode": "backward"
                        },
                        {
                            "step": "month",
                            "count": 6,
                            "label": "6 mo",
                            "stepmode": "backward"
                        },
                        {
                            "step": "year",
                            "count": 1,
                            "label": "1 yr",
                            "stepmode": "backward",
                        },
                        {
                            "step": "year",
                            "count": 1,
                            "label": "YTD",
                            "stepmode": "todate"
                        },
                        {
                            "step": "all"
                        }
                    ],
                }
            },
            "yaxis": {
                "title": "Price",
                "domain": [
                    0,
                    1
                ]
            },
            "margin": {
                "b": 40,
                "l": 60,
                "r": 0,
                "t": 25
            }
        }
    }
    return fig_data


def get_portfolio_figdata_helper(data):
    price = data['return_p']
    baseline = data['return_b']
    trace_p = go.Scatter(x=price.index, y=price, name="returns")
    trace_b = go.Scatter(x=baseline.index, y=baseline, name="baseline")
    fig_data = {
        'data': [trace_p, trace_b],
        "layout": {
            "legend": {'x': 0.8, 'y': 0.8},
            "title": {
                'text': "Portfolio backtest results",
                'xanchor': 'center',
                'yanchor': 'bottom',
                'xref': 'paper'
            },
            "xaxis": {
                "type": "date",
                "title": "Date",
                "domain": [0, 1],
                "rangeslider": {
                    "visible": True
                },
                "rangeselector": {
                    "buttons": [
                        {
                            "step": "month",
                            "count": 1,
                            "label": "1 mo",
                            "stepmode": "backward"
                        },
                        {
                            "step": "month",
                            "count": 3,
                            "label": "3 mo",
                            "stepmode": "backward"
                        },
                        {
                            "step": "month",
                            "count": 6,
                            "label": "6 mo",
                            "stepmode": "backward"
                        },
                        {
                            "step": "year",
                            "count": 1,
                            "label": "1 yr",
                            "stepmode": "backward",
                        },
                        {
                            "step": "year",
                            "count": 1,
                            "label": "YTD",
                            "stepmode": "todate"
                        },
                        {
                            "step": "all"
                        }
                    ],
                }
            },
            "yaxis": {
                "title": "Price",
                "domain": [
                    0,
                    1
                ]
            },
            "margin": {
                "b": 40,
                "l": 60,
                "r": 0,
                "t": 25
            }
        }
    }
    return fig_data


def get_portfolio_figdata(codes):
    with open(DATA_PATH.joinpath('date.csv')) as f:
        start_end = pd.read_csv(f, index_col=0)
    with open(DATA_PATH.joinpath('adjusted_net_value.csv')) as f:
        nav = pd.read_csv(f, index_col=0)
    print("Getting portfolio backtest results...")

    start = time()
    data = get_performance(nav, start_end, codes, fixed='sharpe')
    print("Done: %.2fs elapsed" % (time() - start))
    fig_data = get_portfolio_figdata_helper(data)
    results = data['index']

    index_df = pd.DataFrame(index=["Annu. return", "Alpha", "Win Rate",
                                   "Max drawdown", "Sharpe Ratio", "Sortino Ratio"])
    for k, v in results.items():
        index_df[k] = parse_info(v)
    return fig_data, index_df


def parse_relaydata(start_date_str, end_date_str):
    """

    :param start_date_str:
    :param end_date_str:
    :return:
        one of the following:
            "1", "3", "6", "12": number of months
            "ytd": year to date
            "all"
    """
    start, end = parse_date(start_date_str), parse_date(end_date_str)
    delta = round((end - start).days / 30)
    if start_date_str == '2018-01-01':
        delta = 'ytd'
    elif delta > 12:
        delta = 'all'
    print("Start: {}, end: {}".format(start, end))
    print("OK", delta)
    return str(delta)


if __name__ == '__main__':
    import dash
    import dash_core_components as dcc
    import dash_html_components as html
    from dash.exceptions import PreventUpdate
    from dash.dependencies import Input, Output

    fig_data = get_stock_figdata('519095')
    # fig = go.Figure(fig_data)
    # fig.show()
    app = dash.Dash(__name__)
    app.layout = html.Div(children=[
        html.H1(children='Hello Dash'),
        dcc.Store(id="info_data"),
        dcc.Input(id='code', type='text', placeholder='code'),
        dcc.Input(id='portfolio', type='text', placeholder='portfolio'),
        html.Div([
            html.H2("Blank space", className="four columns"),
            dcc.Graph(
                id='portfolio_graph', figure=fig_data,
                className="six columns"),
            html.Div(id="info", className="two columns")
        ], id="box", className="row"),
        dcc.Graph(id='price_graph', figure=fig_data),
        html.H2(children='Graph relayout data'),
    ])


    @app.callback(
        [Output('portfolio_graph', 'figure'),
         Output("info_data", "data")],
        [Input('portfolio', 'value')]
    )
    def update_profile(value):
        if value is None:
            print("None")
            raise PreventUpdate("Empty")
        codes = value.split()
        print("Updating portfolio graph...", codes)
        fig_data, index = get_portfolio_figdata(codes)
        return fig_data, index.to_json()
        # raise PreventUpdate("Nothing")


    @app.callback(
        [Output("price_graph", "figure")],
        [Input("code", "value")]
    )
    def update_price_graph(code):
        if code is None:
            raise PreventUpdate()
        print("Updating price graph...")
        return get_stock_figdata(code)


    @app.callback(
        [Output('info', 'children')],
        [Input("portfolio_graph", "relayoutData"),
         Input("info_data", "data")]
    )
    def update_info(data, info):
        print("Updating info...")
        if data and 'xaxis.range[0]' in data:
            start_date = data['xaxis.range[0]']
            end_date = data['xaxis.range[1]']
            if end_date != '2018-12-28':
                print("Don't update!", data['xaxis.range[1]'])
                raise PreventUpdate("Nothing changed")
            delta = parse_relaydata(start_date, end_date)
            info_tbl = pd.read_json(info)
            tbl = pd.concat((info_tbl[delta], info_tbl["all"]), axis=1)
            return [generate_table(tbl)]
        if info:
            info_tbl = pd.read_json(info)
            tbl = pd.concat((info_tbl["3"], info_tbl["all"]), axis=1)
            return [generate_table(tbl)]
        raise PreventUpdate("None")


    app.run_server(debug=True)

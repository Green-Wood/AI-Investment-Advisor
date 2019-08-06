import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
from time import time

from plots.backtesting import get_performance

parse_date = lambda d: datetime.strptime(d, "%Y-%m-%d")


def construct_traces(code):
    df0 = pd.read_csv("../data/adjusted_net_value.csv", parse_dates=["datetime"], index_col=0)
    upper = pd.read_csv("../data/yhat_upper_total.csv")
    lower = pd.read_csv("../data/yhat_lower_total.csv")
    df1 = pd.read_csv("../data/yhat_total.csv", parse_dates=["datetime"])
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
            }
            # "margin": {
            #     "b": 40,
            #     "l": 60,
            #     "r": 10,
            #     "t": 25
            # }
        }
    }
    return fig_data


def get_portfolio_figdata_helper(data):
    price = data['return_p']
    baseline = data['return_b']
    trace_p = go.Scatter(x=price.index, y=price, name="net value")
    trace_b = go.Scatter(x=baseline.index, y=baseline, name="baseline")
    fig_data = {
        'data': [trace_p, trace_b],
        "layout": {
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
            }
            # "margin": {
            #     "b": 40,
            #     "l": 60,
            #     "r": 10,
            #     "t": 25
            # }
        }
    }
    return fig_data


def get_portfolio_figdata(codes):
    with open('../data/date.csv') as f:
        start_end = pd.read_csv(f, index_col=0)
    with open('../data/adjusted_net_value.csv') as f:
        nav = pd.read_csv(f, index_col=0)
    print("Getting portfolio backtest results...")

    start = time()
    data = get_performance(nav, start_end, codes, fixed='sharpe')
    print("Done: %.2fs elapsed" % (time() - start))
    fig_data = get_portfolio_figdata_helper(data)
    return fig_data, data['index']


def parse_relaydata(start_date_str, end_date_str):
    """

    :param start_date_str:
    :param end_date_str:
    :return:
        one of the following:
            1, 3, 6, 12: number of months
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
    return delta


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

        dcc.Input(id='input', type='text'),

        dcc.Graph(
            id='profile_graph', figure=fig_data),

        html.H2(children='Graph relayout data'),
        html.H3(id='info'),
        dcc.Store(id='single'),
        dcc.Store(id="portfolio_data")
    ])


    @app.callback(
        [Output('profile_graph', 'figure'),
         Output('single', 'data'), Output('portfolio_data', 'data')],
        [Input('input', 'value')]
    )
    def update_profile(value):
        print("OK")
        if value is None:
            print("None")
            raise PreventUpdate("Empty")
        codes = value.split()
        if len(codes) == 1:
            print("Single", codes[0])
            return get_stock_figdata(codes[0]), True, None
        print(codes)
        fig_data, index = get_portfolio_figdata(codes)
        return fig_data, False, index
        # raise PreventUpdate("Nothing")


    @app.callback(
        [Output('info', 'children')],
        [Input('profile_graph', 'relayoutData'), Input('single', 'data')]
    )
    def update_info(data, single):
        if single is None:
            PreventUpdate()
        print("Updating info...")
        if single:
            print("Single, no updates!")
            raise PreventUpdate("Single!")
        if data and 'xaxis.range[0]' in data:
            start_date = data['xaxis.range[0]']
            end_date = data['xaxis.range[1]']
            if end_date != '2018-12-20':
                print("Don't update!", data['xaxis.range[1]'])
                raise PreventUpdate("Nothing changed")
            delta = parse_relaydata(start_date, end_date)
            return [str(delta)]
        raise PreventUpdate("None")


    app.run_server(debug=True)

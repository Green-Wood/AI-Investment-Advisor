import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output

import pandas as pd
import pathlib

from plots.show_funds import fund_data_layout
from plots.efficirnt_frontier import efficient_frontier_data_layout, best_sharp_ratio

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
# Create global chart template
mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
instruments = pd.read_csv(DATA_PATH.joinpath('instruments.csv'),
                          usecols=['code', 'symbol', 'fund_manager', 'fund_type'])

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=40),
    hovermode="closest",
    plot_bgcolor="#F9F9F9",
    paper_bgcolor="#F9F9F9",
    legend=dict(font=dict(size=10), orientation="h"),
    title="Satellite Overview",
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="light",
        center=dict(lon=-78.05, lat=42.54),
        zoom=7,
    ),
)

config = {
    'risk_range': range(0, 7)
}

# Create app layout
app.layout = html.Div(
    [
        dcc.Store(id="aggregate_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        html.Div(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("logo.jpg"),
                            id="plotly-image",
                            style={
                                "height": "80px",
                                "width": "auto",
                                "margin-bottom": "25px",
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.H3(
                                    "AI-Investment Advisor",
                                    style={"margin-bottom": "0px"},
                                ),
                                html.H5(
                                    "Deecamp 36", style={"margin-top": "0px"}
                                ),
                            ]
                        )
                    ],
                    className="one-half column",
                    id="title",
                ),
                html.Div(
                    [
                        html.A(
                            html.Button("Learn More", id="learn-more-button"),
                            href="https://plot.ly/dash/pricing/",
                        )
                    ],
                    className="one-third column",
                    id="button",
                ),
            ],
            id="header",
            className="row flex-display",
            style={"margin-bottom": "25px"},
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.P(
                            "Choose your risk:",
                            className="control_label",
                        ),
                        dcc.Slider(
                            id="risk_slider",
                            min=min(config['risk_range']),
                            max=max(config['risk_range']),
                            value=min(config['risk_range']),
                            marks={i: '{}'.format(i) for i in config['risk_range']},
                            className="dcc_control",
                        ),
                        html.H5("Fund list", style={
                            'margin-top': '25px',
                            'text-align': 'center'
                        }),
                        dash_table.DataTable(
                            data=instruments.to_dict('records'),
                            columns=[{"name": i, "id": i} for i in instruments.columns],
                            fixed_rows={'headers': True, 'data': 0},
                            page_action="native",
                            page_current=0,
                            page_size=15,
                        )
                    ],
                    className="pretty_container four columns",
                    id="cross-filter-options",
                ),
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [html.H6(id="fund_text", children='1234'), html.P("No. of Funds")],
                                    id="wells",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="return_text", children='23M'), html.P("Return")],
                                    id="gas",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="volatility_text", children='23M'), html.P("Volatility")],
                                    id="oil",
                                    className="mini_container",
                                ),
                                html.Div(
                                    [html.H6(id="sharp_text", children='23M'), html.P("Sharp Ratio")],
                                    id="water",
                                    className="mini_container",
                                ),
                            ],
                            id="info-container",
                            className="row container-display",
                        ),
                        html.Div(
                            # 基金收益图
                            [dcc.Graph(id="profile_graph")],
                            id="countGraphContainer",
                            className="pretty_container",
                        ),
                    ],
                    id="right-column",
                    className="eight columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    # 基金的二维嵌入
                    [dcc.Graph(id="fund_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    # 雷达图
                    [dcc.Graph(id="radar_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    # 效用边界
                    [dcc.Graph(id="efficient_frontier_graph")],
                    className="pretty_container seven columns",
                ),
                html.Div(
                    # 关系网络
                    [dcc.Graph(id="network_graph")],
                    className="pretty_container five columns",
                ),
            ],
            className="row flex-display",
        ),
    ],
    id="mainContainer",
    style={"display": "flex", "flex-direction": "column"},
)


# helper function

def get_efficient_frontier(selected_code, click_code):
    """
    根据所选中的和点击的基金code获得效用边界的布局
    :param selected_code:
    :param click_code:
    :return:
    """
    ids = selected_code + click_code
    if len(ids) == 0:
        return efficient_frontier_data_layout('all')
    return efficient_frontier_data_layout(ids)


def get_best_sharp_ratio():
    """
    返回最高的sharp ratio的相关数据
    :return: Return、Volatility、SharpRatio, weights
    """
    ret, vol, sharp, weight = best_sharp_ratio()
    ret = '%.5f' % ret
    vol = '%.5f' % vol
    sharp = '%.5f' % sharp
    return ret, vol, sharp, weight


# @app.callback(
#     [Output('show-funds', 'figure'),
#      Output('risk-text', 'children')],
#     [Input('risk-slider', 'value')]
# )
# def update_risk(risk_val):
#     return fund_data_layout(risk_val), '您选择的风险值为: {}'.format(risk_val)
#
#
@app.callback(
    [Output('efficient_frontier_graph', 'figure'),
     Output('fund_text', 'children'),
     Output('return_text', 'children'),
     Output('volatility_text', 'children'),
     Output('sharp_text', 'children')],
    [Input('fund_graph', 'selectedData'),
     Input('fund_graph', 'clickData')]
)
def update_select(selectedData, clickData):
    selected_points = set(selectedData['points']) if selectedData is not None else set()
    click_points = set(clickData['points']) if clickData is not None else set()
    selected_code = [p['code'] for p in selected_points]
    click_code = [p['code'] for p in click_points]
    efficient_frontier_data = get_efficient_frontier(selected_code, click_code)
    ret, vol, sharp, weight = get_best_sharp_ratio()
    return efficient_frontier_data, len(weight), ret, vol, sharp


if __name__ == '__main__':
    app.run_server(debug=True)

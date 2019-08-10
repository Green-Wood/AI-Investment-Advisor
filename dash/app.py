import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import plotly.graph_objs as go

import pandas as pd
import json
import pathlib

from plots.plot_efficient_frontier import efficient_frontier_data_layout, get_fixed_ans

from plots.plot_heatmap import plot_heatmap_dendrogram
from plots.ploy_sna import ploy_sna_pic
from plots.show_barpolar import show_barpolar
from plots.plot_fund_graph import plot_fund
from plots.plot_profile import get_portfolio_figdata, get_stock_figdata, parse_relaydata, generate_table

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

server = app.server

# Create global chart template
mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("data").resolve()
instruments = pd.read_csv(DATA_PATH.joinpath('sna_portfolio_data.csv'), encoding='gb18030',
                          usecols=['code', 'symbol', 'fund_type'])

factors_list = ['fund_type_factors', 'issuer_count_factors', 'fund_manager_factors', 'fund_manager_numbers_factors',
                'manager_past_factors', 'benchmark_embedding_factors']
chinese_factor_list = ['基金类型', '公司规模', '基金经理', '经理基金数', '经理历史收益', 'Benchmark']
english_factor_list = ['fund type', 'company size', 'fund manager', 'manage No.', 'history return', 'benchmark']

layout = dict(
    autosize=True,
    automargin=True,
    margin=dict(l=30, r=30, b=20, t=10),
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
        dcc.Store(id="info_data"),
        html.Div(
            [
                html.Div(
                    # 用户选择区
                    [
                        html.P(
                            "Choose your risk",
                            className="control_label",
                            style={
                                'text-align': 'center'
                            }
                        ),
                        dcc.Slider(
                            id="risk_slider",
                            min=min(config['risk_range']),
                            max=max(config['risk_range']),
                            value=min(config['risk_range']),
                            marks={i: '{}'.format(i) for i in config['risk_range']},
                            className="dcc_control",
                        ),
                        dcc.Graph()
                    ],
                    id='user_choose_playground',
                    className='pretty_container four columns',
                ),
                html.Div([
                    # 基金收益图
                    html.Div([dcc.Graph(id='portfolio_graph',
                                        className="six columns"),
                              html.Div(id="info", className="two columns")
                              ],
                             className='eight columns'),
                    dcc.Graph(id='price_graph'),
                ], className="pretty_container eight columns"
                )
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    # 相关系数
                    [dcc.Graph(id="corr_graph")],
                    className="pretty_container five columns",
                ),
                html.Div(
                    # 效用边界
                    [dcc.Graph(id="efficient_frontier_graph")],
                    className="pretty_container four columns",
                ),
                html.Div(
                    # 2048
                    [dcc.Graph(id="treemap_graph")],
                    className="pretty_container four columns",
                ),
            ],
            className="row flex-display",
        ),
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
                                "margin-left": "25px",
                                'textAlign': 'center'
                            },
                        )
                    ],
                    className="one-third column",
                ),
                html.Div(
                    [
                        html.H3(
                            "AI-Investment Advisor",
                            style={"margin-bottom": "0px"},
                        ),
                        html.H5(
                            "Deecamp 36", style={"margin-top": "0px"}
                        ),
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
        ),
        # 储存用户选择的基金列表
        dcc.Store(id='user_list'),
        # 储存用户点选的单只基金
        dcc.Store(id='user_choose'),
        # 储存用户所选择的基金的最佳策略
        dcc.Store(id='user_weight'),
        # 储存用户的最佳权重字典
        dcc.Store(id='best_weight')
    ],
    id="mainContainer",
    # style={"display": "flex", "flex-direction": "column"},
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


def get_fund_table(dict_weight):
    """
    根据权值字典获得fund_table
    :param dict_weight:
    :return:
    """
    weight_df = pd.DataFrame.from_dict(dict_weight, orient='index', columns=['weight'])
    weight_df.reset_index(inplace=True)
    weight_df['index'] = weight_df['index'].astype(int)
    ins_wei_df = instruments.merge(weight_df, left_on='code', right_on='index')
    ins_wei_df = ins_wei_df.drop(['index'], axis=1)
    ins_wei_df = ins_wei_df.sort_values('weight', ascending=False)
    ins_wei_df['weight'] = ins_wei_df['weight'].apply(lambda x: '{:.5f}%'.format(x * 100))
    return ins_wei_df


best_weight = dict()


@app.callback(
    Output('user_choose', 'data'),
    [Input('user_list', 'data')]  # 添加input
)
def update_user_choose():
    """
    在基金推荐中点选（高亮）,在基金详情块上点选（高亮）,在二环上点选（高亮）, 更新用户所点选的单个基金
    :param risk_val:
    :return:
    """
    pass


@app.callback(
    Output('best_weight', 'data'),
    [Input('risk_slider', 'value')]
)
def update_best_weight(risk_val):
    """
    根据risk值来更新最佳的分配，记得更新全局变量
    :param risk_val:
    :return:
    """
    pass


@app.callback(
    Output('user_list', 'data'),
    [Input('risk_slider', 'value')]
)
def update_user_list():
    """
    risk值、在基金详情块上删除、在基金推荐中新增 来更新用户选择的基金列表
    :param:
    :return:
    """
    pass


@app.callback(
    Output('user_weight', 'data'),
    [Input('risk_slider', 'value'),
     Input('user_list', 'data')]
)
def update_user_weight():
    """
    risk值，用户所选择的基金列表 来更新 用户所选基金的权重字典
    :param:
    :return:
    """
    pass

#
# @app.callback(
#     Output(),
#     [Input()]
# )
# def update_detail():
#     """
#     在一环上点选。来显示属于该风险的四个基金、显示推荐的相关基金
#     :return:
#     """
#     pass

#
# @app.callback(
#     Output(),
#     [Input('user_list', 'data')]
# )
# def update_ring_two():
#     """
#     用户所选择的列表 更新  二环图
#     :return:
#     """
#     pass


@app.callback(
    Output('treemap_graph', 'figure'),
    [Input('best_weight', 'data')]
)
def update_treemap():
    """
    最佳基金权重字典 更新 2048
    :return:
    """
    pass


@app.callback(
    [Output('portfolio_graph', 'figure'),
     Output("info_data", "data")],
    [Input('user_list', 'data')]
)
def update_profile(codes):
    if codes is None:
        print("None")
        raise PreventUpdate("Empty")
    print("Updating portfolio graph...", codes)
    fig_data, index = get_portfolio_figdata(codes)
    return fig_data, index.to_json()
    # raise PreventUpdate("Nothing")


@app.callback(
    [Output("price_graph", "figure")],
    [Input("user_choose", "data")]
)
def update_price_graph(code):
    if code is None:
        raise PreventUpdate()
    print("Updating price graph...")
    return get_stock_figdata(code)


#
#
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


@app.callback(
    Output('corr_graph', 'figure'),
    [Input('user_list', 'data')]
)
def update_corr(choose_list):
    """
    选中的基金列表 -> 热力图
    :return:
    """
    choose_list = ['519661', '000061', '398061', '519995', '470059']
    if choose_list is None:
        choose_list = best_weight.keys()
    return plot_heatmap_dendrogram(choose_list)


@app.callback(
    Output('efficient_frontier_graph', 'figure'),
    [Input('user_list', 'data')]
)
def update_efficient_frontier(choosed_list):
    """
    选中的基金列表 -> 有效边界
    :return:
    """
    data_layout = efficient_frontier_data_layout(choosed_list)
    return data_layout


if __name__ == '__main__':
    app.run_server(debug=True)

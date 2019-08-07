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

from plots.efficirnt_frontier import efficient_frontier_data_layout, get_fixed_ans
from plots.ploy_sna import ploy_sna_pic
from plots.show_barpolar import show_barpolar
from plots.plot_fund_graph import plot_fund
from plots.plot_profile import get_portfolio_figdata, get_stock_figdata, parse_relaydata

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
        dcc.Store(id="single"),
        dcc.Store(id="portfolio_data"),
        # empty Div to trigger javascript file for graph resizing
        html.Div(id="output-clientside"),
        # html.Div(
        #     [
        #         html.Div(
        #             [
        #                 html.Div(
        #                     [
        #                         html.Div(
        #                             [html.H6(id="fund_text", children='1234'), html.P("No. of Funds")],
        #                             id="wells",
        #                             className="mini_container",
        #                         ),
        #                         html.Div(
        #                             [html.H6(id="return_text", children='23M'), html.P("Annualized Return")],
        #                             id="gas",
        #                             className="mini_container",
        #                         ),
        #                         html.Div(
        #                             [html.H6(id="volatility_text", children='23M'), html.P("Volatility")],
        #                             id="oil",
        #                             className="mini_container",
        #                         ),
        #                         html.Div(
        #                             [html.H6(id="sharp_text", children='23M'), html.P("Sharp Ratio")],
        #                             id="water",
        #                             className="mini_container",
        #                         ),
        #                     ],
        #                     id="info-container",
        #                     className="row container-display",
        #                 ),
        #                 html.Div(
        #                     [
        #                         html.Div(
        #                             [html.H6(id="alpha_text", children='示例'), html.P("Alpha")],
        #                             id="alpha",
        #                             className="mini_container",
        #                         ),
        #                         html.Div(
        #                             [html.H6(id="win_rate_text", children='示例'), html.P("Win Rate")],
        #                             id='win_rate',
        #                             className="mini_container",
        #                         ),
        #                         html.Div(
        #                             [html.H6(id="max_drawdown_text", children='示例'), html.P("Max Drawdown")],
        #                             id="max_drawdown",
        #                             className="mini_container",
        #                         ),
        #                         html.Div(
        #                             [html.H6(id="sortino_ratio_text", children='示例'), html.P("Sortino Ratio")],
        #                             id="sortino_ratio",
        #                             className="mini_container",
        #                         )
        #                     ],
        #                     id="profit_container",
        #                     className="row container-display",
        #                 ),
        #
        #             ],
        #             id="right-column",
        #             className="eight columns",
        #         ),
        #     ],
        #     className="row flex-display",
        # ),
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
                    className='pretty_container six columns',
                ),
                html.Div(
                    # 基金收益图
                    [
                        dcc.Graph(id="profile_graph")
                    ],
                    className='pretty_container six columns'
                )
            ],
            className="row flex-display",
        ),
        html.Div(
            [
                html.Div(
                    # 相关系数
                    [dcc.Graph(id="corr_graph")],
                    className="pretty_container four columns",
                ),
                html.Div(
                    # 效用边界
                    [dcc.Graph(id="efficient_frontier_graph")],
                    className="pretty_container four columns",
                ),
                html.Div(
                    # 2048
                    [dcc.Graph(id="network_graph")],
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
        dcc.Store(id='fund_list'),
        # 储存当前状态下的基金权重
        dcc.Store(id='fund_weights'),
        dcc.Store(id='lala')
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


# @app.callback(
#     [Output('fund_weights', 'data'),
#      Output('fund_text', 'children'),
#      Output('return_text', 'children'),
#      Output('volatility_text', 'children'),
#      Output('sharp_text', 'children')],
#     [
#         # Input('fund_list', 'children'),
#         Input('risk_slider', 'value')]
# )
# def update_weights(risk_val):
#     """
#     拉动risk滑块 -> 基金的权重
#     :param fund_list:
#     :param risk_val:
#     :return:
#     """
#     risk_val = risk_val / 100
#     ret, vol, sharp, dict_weights = get_fixed_ans(fixed='volatility', value=risk_val)
#     return dict_weights, len(dict_weights), ret, vol, sharp
#
#
# @app.callback(
#     Output('fund_list', 'data'),
#     [Input('fund_graph', 'selectedData'),
#      Input('fund_table', "derived_virtual_data"),
#      Input('fund_table', 'derived_virtual_selected_rows')]
# )
# def update_fund_list(selectedData, derived_virtual_data, selected_row):
#     """
#     二维图中选取 -> 选中的基金列表
#     基金列表中选取 -> 选中的基金列表
#     :return:
#     """
#     if selectedData is None and (selected_row == None or len(selected_row) == 0):
#         ret, risk, sharpe, weights = get_fixed_ans()
#         columns = [key for key, v in weights.items() if v > 1e-8]
#         return columns
#     selected_code = set()
#     row_code = set()
#     if len(selected_row) != 0:
#         row_code = {derived_virtual_data[x]['code'] for x in selected_row}
#     if selectedData is not None:
#         selected_code = {p['customdata'] for p in selectedData['points']}
#     code = row_code | selected_code
#     code = ['0' * (6 - len(str(x))) + str(x) for x in code]
#     return code
#
#
# # @app.callback(
# #     Output('profile_graph', 'figure'),
# #     [Input('fund_list', 'children')]
# # )
# # def update_profile(choosed_list):
# #     """
# #     选中的基金列表 -> 回测、单位净值
# #     :return:
# #     """
# #     pass
#
# @app.callback(
#     [Output('profile_graph', 'figure'),
#      Output('single', 'data'), Output('portfolio_data', 'data')],
#     [Input('fund_list', 'data')]
# )
# def update_profile(codes):
#     print("Updating profile...")
#     if codes is None:
#         print("None")
#         raise PreventUpdate("Empty")
#     # codes = value.split()
#     if len(codes) == 1:
#         print("Single", codes[0])
#         return get_stock_figdata(codes[0]), True, None
#     fig_data, index = get_portfolio_figdata(codes)
#     return fig_data, False, index
#
#
# @app.callback(
#     [Output('lala', 'data')],
#     [Input('profile_graph', 'relayoutData'), Input('single', 'data')]
# )
# def update_info(data, single):
#     print("Updating info...")
#     if single:
#         print("Single")
#         raise PreventUpdate("Single!")
#     if data and 'xaxis.range[0]' in data:
#         start_date = data['xaxis.range[0]']
#         end_date = data['xaxis.range[1]']
#         if end_date != '2018-12-28':
#             print("Don't update!", data['xaxis.range[1]'])
#             raise PreventUpdate("Nothing changed")
#         delta = parse_relaydata(start_date, end_date)
#         return [delta]
#     raise PreventUpdate("None")
#
#
# @app.callback(
#     Output('fund_table', 'data'),
#     [
#         # Input('fund_list', 'children'),
#         Input('fund_weights', 'data')]
# )
# def update_fund_table(fund_weights):
#     """
#     基金权重，选中的基金列表 -> fund table
#     :return:
#     """
#     if fund_weights is None:
#         ret, risk, sharpe, weights = get_fixed_ans(fixed='volatility', value=0)
#         fund_weights = weights
#     df = get_fund_table(fund_weights)
#     return df.to_dict('records')
#
#
# @app.callback(
#     Output('radar_graph', 'figure'),
#     [Input('fund_list', 'data'),
#      Input('fund_weights', 'data')]
# )
# def update_pie(choosed_list, fund_weights):
#     """
#     基金权重，选中的基金列表 -> 饼图
#     :return:
#     """
#     if choosed_list is None or fund_weights is None:
#         return None
#     selected_weights = {
#         k: v
#         for k, v in fund_weights.items() if k in choosed_list
#     }
#     return show_barpolar(selected_weights)
#
#
# @app.callback(
#     Output('fund_graph', 'figure'),
#     [Input('fund_list', 'data'),
#      Input('fund_weights', 'data'),
#      Input('factors_check_list', 'value')]
# )
# def update_fund_graph(choosed_list, fund_weights, factors):
#     """
#     基金权重，选中的基金列表 -> 二维图
#     :return:
#     """
#     if fund_weights is None:
#         return None
#     if len(factors) == 0:
#         factors = factors_list
#     fac_dic = {
#         i: True if i in factors else False
#         for i in factors_list
#     }
#     selected_weights = {
#         k: v
#         for k, v in fund_weights.items() if k in choosed_list
#     }
#     return plot_fund(fac_dic, selected_weights)
#
#
# @app.callback(
#     Output('efficient_frontier_graph', 'figure'),
#     [Input('fund_list', 'data')]
# )
# def update_efficient_frontier(choosed_list):
#     """
#     选中的基金列表 -> 有效边界
#     :return:
#     """
#     data_layout = efficient_frontier_data_layout(choosed_list)
#     return data_layout
#
#
# @app.callback(
#     Output('network_graph', 'figure'),
#     [Input('fund_list', 'data')]
# )
# def update_network(choosed_list):
#     """
#     选中的基金列表 -> 网络关系图
#     :return:
#     """
#     return ploy_sna_pic(choosed_list)


if __name__ == '__main__':
    app.run_server(debug=True)

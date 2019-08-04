# coding: utf-8
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import pathlib


def plot_fund(node_weight):

    PATH = pathlib.Path(__file__).parent.parent
    DATA_PATH = PATH.joinpath("data").resolve()

    fund_pos = pd.read_csv(DATA_PATH.joinpath('fund_graph_coordinate.csv'), index_col=0, encoding = 'gb18030')

    node_weight_df = pd.DataFrame.from_dict(node_weight, orient='index')
    node_weight_df.columns = ['fund_weight_true']
    node_weight_df.index = node_weight_df.index.astype(int)

    plot_fund_dot = pd.merge(node_weight_df, fund_pos, left_index=True, right_index=True, how='left')
    plot_fund_dot['fund_type_color'] = plot_fund_dot['fund_type']

    plot_fund_dot['fund_weight'] = plot_fund_dot['fund_weight_true']

    plot_not_fund_dot = fund_pos.drop(node_weight_df.index)
    plot_not_fund_dot['fund_type_color'] = 'Unselected'
    plot_not_fund_dot['fund_weight_true'] = 0
    plot_not_fund_dot['fund_weight'] = 1e-15

    plot_data = pd.concat([plot_fund_dot, plot_not_fund_dot])

    plot_data["fund_weight"] = np.log10(plot_data["fund_weight"])
    plot_data["fund_weight"] = plot_data["fund_weight"] - plot_data["fund_weight"].min() + 10

    plot_data['fund_weight_true'] = plot_data['fund_weight_true'].apply(lambda x: format(x, '.5%'))

    plot_data['show_text'] = '基金代码：' + plot_data.index.map(str) + '<br>' + '基金名称：' + plot_data['symbol'] + '<br>' + '基金占比：' + plot_data['fund_weight_true'] + '<br>' + '基金类型：' + plot_data['fund_type']

    fig = go.Figure()
    colors = {'Stock': '#5f27cd',
              'Bond': '#ee5253',
              'Related': '#10ac84',
              'QDII': '#f368e0',
              'Other': '#ff9f43',
              'Hybrid': '#01a3a4',
              'Unselected': '#8395a7'
              }

    add_order = list(set(plot_data['fund_type_color'].values))
    add_order.sort(reverse=True)

    for node_i in add_order:
        fig.add_trace(go.Scatter(
            x=plot_data[plot_data['fund_type_color'] == node_i]['X'],
            y=plot_data[plot_data['fund_type_color'] == node_i]['Y'],
            name=node_i,
            mode="markers",
            hoverinfo='text',  # 隐藏坐标

            text=plot_data[plot_data['fund_type_color'] == node_i]['show_text'],

            marker=go.scatter.Marker(
                size=plot_data[plot_data['fund_type_color'] == node_i]['fund_weight'],
                color=colors[node_i],
                opacity=0.6
            ),
        ))

    fig.update_layout(go.Layout(
                    title='<br>Fund Embedding',
                    titlefont_size=20,
                    plot_bgcolor='white',
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                 ))

    return fig


if __name__ == '__main__':
    node_weight = {'100066': 0.016735720134814773, '100068': 0.015433163091007545,
                   '161603': 1.355455236331784e-11, '166903': 1.6658634581675288e-10,
                   '166904': 0.003912742925666486, '519669': 1.8326092766475134e-10,
                   '161693': 1.2050684315404923e-11, '159934': 2.0920509354101373e-10,
                   '166902': 4.82377878227999e-10, '650002': 3.172654585193117e-07,
                   '161120': 5.563456855842489e-11, '161618': 1.563237703114718e-11,
                   '163211': 4.547423075756075e-11, '161911': 8.272047412068348e-11,
                   '000129': 0.048343510672935484, '160129': 5.744244596864218e-11,
                   '000216': 7.362595242896624e-09, '000116': 0.014914699696184615,
                   '000187': 2.325755083426496e-10, '518880': 1.7233481703454906e-10,
                   '000428': 4.803525289659809e-10, '000128': 0.04890193565627362,
                   '160128': 9.59363262903844e-11, '000217': 0.0027213470675978534,
                   '161117': 1.0527176846629606e-05, '163210': 6.156477541037609e-11,
                   '160719': 0.0026541758177289513, '161119': 5.5560454854493054e-11,
                   '161619': 1.5499763299699786e-11, '040026': 0.022160884296799285,
                   '320021': 9.393603936033154e-12, '000286': 0.007343299976607506,
                   '000186': 2.19187388723884e-11, '000188': 1.232787430445312e-10,
                   '070038': 0.014401680154329828, '518800': 1.9756830171150588e-10,
                   '070009': 0.09879630515116061, '000191': 2.369561148291286e-11,
                   '519662': 0.0012938038642485103, '000396': 0.028647884808778758,
                   '519153': 0.052285140498323994, '070037': 0.01395904628175895,
                   '650001': 0.0019579787433699264, '000139': 3.916984299754435e-10,
                   '519152': 0.04714530448166936, '519663': 0.002276766084421897,
                   '040046': 4.23717714128679e-11, '000346': 0.047698168826055216,
                   '040041': 0.024062709004198567, '000148': 3.461020338030308e-11,
                   '000084': 0.053933088308166795, '519024': 0.006770926347552023,
                   '519723': 2.4920602514125483e-10, '519023': 0.005523198115898473,
                   '000085': 0.05052074217786705, '040040': 0.02226569442059756,
                   '000347': 0.04107629056161011, '161614': 2.258008455907503e-11,
                   '519725': 1.4108251481358556e-08}
    fig = plot_fund(node_weight)
    fig.show()

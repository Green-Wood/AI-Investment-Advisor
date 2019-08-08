import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.figure_factory as ff
from pypfopt import risk_models
import pathlib
from scipy.spatial.distance import pdist, squareform
import matplotlib.pyplot as plt

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()
path_adjusted_net_value = DATA_PATH.joinpath('adjusted_net_value.csv')
path_instrument = DATA_PATH.joinpath('instruments.csv')

font_size = 8
# 步长和窗口大小
window = 30
step = 3


# todo: 字体大小 fig.layout.annotations[i].font.size


def mean_solve(df: pd.DataFrame):
    window = 2
    for i in df.columns.values:
        df['tmp'] = df[i]
        df[i].iloc[window] = np.mean(df['tmp'][:window])
        df.loc[window:, i] = (df.loc[window:, i].fillna(df['tmp'])
                              .ewm(adjust=False, alpha=(window - 1.) / window).mean())
    df.drop('tmp', axis=1)
    return df


def get_corr(org_data):
    cov = risk_models.CovarianceShrinkage(org_data).ledoit_wolf()
    var = np.eye(cov.shape[0]) * cov
    std = np.power(var, 0.5)
    I = np.linalg.inv(std)
    corr = I.dot(cov).dot(I)
    return corr


def plot_heatmap(codelist: list):
    """
    :param (list) codelist:基金代码列表
    :return: (dict) fig{
                    'data':
                    'layout':
            }
    """
    df = pd.read_csv(path_adjusted_net_value)
    df = df[codelist]
    codes = df.columns.values
    z = get_corr(df)
    zmin = np.min(z)
    # 保留两位数作为文本显示
    z2 = np.around(z, decimals=2)
    strs = [code + '' for code in codelist]
    z_text = []
    # 变为下三角矩阵
    for i in range(len(z)):
        z_text.append([])
        for j in range(len(z[i])):
            if j < (i + 1):
                z_text[i].append(str(z2[i, j]))
            else:
                z_text[i].append('')
                z[i, j] = zmin
    # customdatas  两个对应基金号,以空格隔开,格式为 'code code'
    customdatas = []
    for i in range(len(z)):
        customdatas.append([])
        customdatas[i] = [(str(codes[i]) + ' ' + str(codes[j])) for j in range(len(z[i]))]
    fig = ff.create_annotated_heatmap(z,
                                      annotation_text=z_text,
                                      colorscale='Viridis',
                                      showscale=True,
                                      hoverinfo='text',
                                      text=z_text,
                                      customdata=customdatas,
                                      x=strs,
                                      y=strs
                                      )
    # 变换字体大小
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = font_size
    # fig.show()
    return {
        'data': fig.data,
        'layout': fig.layout
    }


def plot_time_corr(codes: str):
    """
    :param (str) codes: 格式 'code1 code2'
                        eg:'519661 257050'
    :return: (dict) fig{
                    'data':
                    'layout':
            }
    """
    org_data = pd.read_csv(path_adjusted_net_value)
    org_dates = org_data['datetime']
    codes = codes.split(' ')
    data = org_data[[codes[0], codes[1]]]
    # data = data.diff(1)
    # data = data.dropna()
    data = mean_solve(data)
    corrs = []
    dates = []
    for i in range(window, 1225, step):
        tmp = data[i - window:i]
        dates.append(org_dates[i])
        corrs.append(get_corr(tmp)[1, 0])
    fig = go.Figure(data=go.Scatter(x=dates, y=corrs))
    # fig.show()
    return {
        'data': fig.data,
        'layout': fig.layout
    }


def plot_heatmap_dendrogram(code_list: list):
    """
    :param (list) code_list: 基金代码列表
    :return: (dict) fig{
                    'data':
                    'layout':
            }
    """
    org_data = pd.read_csv(path_adjusted_net_value)
    org_data = org_data[code_list]
    fund_data = pd.read_csv(path_instrument)[['code', 'issuer']]
    strs = [code + '' for code in code_list]
    z = org_data.dropna().as_matrix()
    codes = org_data.columns.values
    data_array = z.T
    labels = codes

    # Initialize figure by creating upper dendrogram
    fig = ff.create_dendrogram(data_array, orientation='bottom', labels=labels)
    for i in range(len(fig['data'])):
        fig['data'][i]['yaxis'] = 'y2'

    # Create Side Dendrogram
    dendro_side = ff.create_dendrogram(data_array, orientation='right')
    for i in range(len(dendro_side['data'])):
        dendro_side['data'][i]['xaxis'] = 'x2'

    # Add Side Dendrogram Data to Figure
    for data in dendro_side['data']:
        fig.add_trace(data)

    # Create Heatmap
    dendro_leaves = dendro_side['layout']['yaxis']['ticktext']
    dendro_leaves = list(map(int, dendro_leaves))
    data_dist = pdist(data_array)
    heat_data = squareform(data_dist)
    heat_data = heat_data[dendro_leaves, :]
    heat_data = heat_data[:, dendro_leaves]
    heat_data_2 = np.round(heat_data, decimals=2)

    texts = np.zeros(shape=(len(code_list), len(code_list)), dtype=list)
    for i in range(len(texts)):
        for j in range(len(texts[i])):
            tmp1 = fund_data[fund_data['code'].isin([code_list[i]])]['issuer'].values[0]
            tmp2 = fund_data[fund_data['code'].isin([code_list[j]])]['issuer'].values[0]
            texts[i, j] = '基金公司1:' + tmp1 + '<br>' + '基金公司2:' + tmp2 + '<br>' + '样本距离' + str(heat_data_2[i, j])
    heatmap = ff.create_annotated_heatmap(heat_data,
                                          annotation_text=heat_data_2,
                                          colorscale='blues',
                                          showscale=True,
                                          hoverinfo='text',
                                          text=texts,
                                          x=strs,
                                          y=strs
                                          )
    heatmap['data'][0]['x'] = fig['layout']['xaxis']['tickvals']
    heatmap['data'][0]['y'] = dendro_side['layout']['yaxis']['tickvals']

    # Add Heatmap Data to Figure
    for data in heatmap['data']:
        fig.add_trace(data)

    # Edit Layout
    fig.update_layout({
        'showlegend': False, 'hovermode': 'closest',
    })
    # Edit xaxis
    fig.update_layout(xaxis={'domain': [.15, 1],
                             'mirror': False,
                             'showgrid': False,
                             'showline': False,
                             'zeroline': False,
                             'ticks': ""})
    # Edit xaxis2
    fig.update_layout(xaxis2={'domain': [0, .15],
                              'mirror': False,
                              'showgrid': False,
                              'showline': False,
                              'zeroline': False,
                              'showticklabels': False,
                              'ticks': ""})

    # Edit yaxis
    fig.update_layout(yaxis={'domain': [0, .85],
                             'mirror': False,
                             'showgrid': False,
                             'showline': False,
                             'zeroline': False,
                             'showticklabels': False,
                             'ticks': ""
                             })
    # Edit yaxis2
    fig.update_layout(yaxis2={'domain': [.825, .975],
                              'mirror': False,
                              'showgrid': False,
                              'showline': False,
                              'zeroline': False,
                              'showticklabels': False,
                              'ticks': ""})
    # fig.update_layout(title={
    #     'text': 'Sure',
    #     'xanchor': 'center',
    #     'yanchor': 'bottom',
    #     'xref': 'paper'
    # })
    # Plot!
    # fig.show()
    fig['layout']['title'] = {
        'text': 'Sure',
        'xanchor': 'center',
        'yanchor': 'bottom',
        'xref': 'paper'
    }
    return fig


if __name__ == '__main__':
    # test demo
    z = np.random.randn(20, 20)
    codes = ['257050', '000395', '000001', '519050']
    fig = plot_heatmap_dendrogram(codes)
    print(fig)
    # codes = '257050 000395'
    # plot_time_corr(codes)

    # org_data = pd.read_csv('../data/adjusted_net_value.csv')
    # org_data = org_data[['519661','257050','510150','377150','510650','510050','519050','270050','000150','519150','310368','686868','519668','000068','100068','519068','470068','000368','000057','080003','180003','550003','450003','213003','110003','630003','000003','620003','610103','161603','519003','090003','540003','630103','700003']]
    # # plot_heatmap_dendrogram(org_data=pd.DataFrame(z))
    # # plot_heatmap_dendrogram(org_data=org_data)
    # corr = get_corr(org_data)
    # print(corr)

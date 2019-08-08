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
font_size = 8
# 步长和窗口大小
window = 30
step = 3
# todo: path_adjusted_net_value  adjusted_net_value.csv文件
# todo: 字体大小 fig.layout.annotations[i].font.size


def mean_solve(df:pd.DataFrame):
    window = 2
    for i in df.columns.values:
        df['tmp'] = df[i]
        df[i].iloc[window] = np.mean(df['tmp'][:window])
        df.loc[window:,i] = (df.loc[window:,i].fillna(df['tmp'])
                                .ewm(adjust=False,alpha=(window - 1.) / window).mean())
    df.drop('tmp',axis=1)
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
    strs = [code+'' for code in codelist]
    z_text=[]
    # 变为下三角矩阵
    for i in range(len(z)):
        z_text.append([])
        for j in range(len(z[i])):
            if j<(i+1):
                z_text[i].append(str(z2[i,j]))
            else:
                z_text[i].append('')
                z[i,j] = zmin
    # customdatas  两个对应基金号,以空格隔开,格式为 'code code'
    customdatas = []
    for i in range(len(z)):
        customdatas.append([])
        customdatas[i] = [(str(codes[i]) + ' ' + str(codes[j])) for j in range(len(z[i]))]
    fig = ff.create_annotated_heatmap(z,
                                      annotation_text=z_text,
                                      colorscale='Greys',
                                      showscale=True,
                                      hoverinfo='all',
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
    org_dates =org_data['datetime']
    codes = codes.split(' ')
    data = org_data[[codes[0],codes[1]]]
    # data = data.diff(1)
    # data = data.dropna()
    data = mean_solve(data)
    corrs = []
    dates = []
    for i in range(window,1225,step):
        tmp = data[i-window:i]
        dates.append(org_dates[i])
        corrs.append(get_corr(tmp)[1,0])
    fig = go.Figure(data=go.Scatter(x=dates, y=corrs))
    # fig.show()
    return {
        'data':fig.data,
        'layout':fig.layout
    }


if __name__ == '__main__':
    # test demo
    z = np.random.randn(20, 20)
    codes = ['257050', '000395','000001', '519050']
    fig = plot_heatmap(codes)
    print(fig)
    codes = '257050 000395'
    plot_time_corr(codes)

    # org_data = pd.read_csv('../data/adjusted_net_value.csv')
    # org_data = org_data[['519661','257050','510150','377150','510650','510050','519050','270050','000150','519150','310368','686868','519668','000068','100068','519068','470068','000368','000057','080003','180003','550003','450003','213003','110003','630003','000003','620003','610103','161603','519003','090003','540003','630103','700003']]
    # # plot_heatmap_dendrogram(org_data=pd.DataFrame(z))
    # # plot_heatmap_dendrogram(org_data=org_data)
    # corr = get_corr(org_data)
    # print(corr)


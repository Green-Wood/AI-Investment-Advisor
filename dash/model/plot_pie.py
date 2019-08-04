import plotly.graph_objects as go
import pandas as pd
from collections import defaultdict


def stat(ratios: dict):
    """
    :param ratios:dict（多只）基金代码:该基金权重
    :return result: dict  基金类型:该类型占比
    """
    table = {}
    with open('../data/fund_type.csv') as f:
        for line in f:
            key, val = line.split()
            table[key] = val
    result = {}
    for k, v in ratios.items():
        type = table[k]
        result[type] = result.get(type, 0) + v
    return result


def get_pie_plot(ratios):
    result = stat(ratios)
    fig = go.Pie(labels=list(result.keys()), values=list(result.values()), hole=.3)
    return {'data': fig}


if __name__ == '__main__':
    # test
    data = {'000001': 0.5,
            '000003': 0.3,
            '000007': 0.2,
            '000028': 0.1,
            '960001': 0.3
            }
    fig_data = get_pie_plot(data)
    fig = go.Figure(fig_data)
    fig.show()

import plotly.graph_objects as go
import pathlib

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()
instruments = DATA_PATH.joinpath('fund_type.csv')


def stat(ratios: dict):
    """
    :param ratios:dict（多只）基金代码:该基金权重
    :return result: dict  基金类型:该类型占比
    """
    table = {}
    with open(instruments) as f:
        for line in f:
            key, val = line.split()
            table[key] = val
    result = {}
    for k, v in ratios.items():
        fund_type = table[k]
        result[fund_type] = result.get(fund_type, 0) + v
    return result


def get_pie_plot(ratios):
    result = stat(ratios)
    myfig = go.Pie(labels=list(result.keys()), values=list(result.values()), hole=.3)
    return {'data': [myfig]}


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

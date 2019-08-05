import plotly.graph_objs as go
from init_optmizer import optimizer
import pathlib
import pandas as pd

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()
instruments = pd.read_csv(DATA_PATH.joinpath('instruments.csv'), usecols=['code', 'symbol', 'fund_type'])


def efficient_frontier_data_layout(id_list):
    if len(id_list) == 1:
        id_list = 'all'
    efficient_data = optimizer.efficient_frontier(id_list)
    return {
        'data': [
            go.Scatter(
                x=efficient_data[1],
                y=efficient_data[0],
                opacity=0.75,
                text=['Sharpe Ratio: {}'.format(x) for x in efficient_data[2]],
                mode='markers+lines',
                marker={
                    'color': efficient_data[2],
                    'colorbar': {
                        'title': 'Sharp Ratio'
                    },
                    'colorscale': 'Viridis',
                }
            ),
        ],
        'layout': {
            'title': {
                'text': 'Efficient Frontier',
                'font': {
                    'size': 30
                }
            },
            'xaxis': {
                'title': 'Annualised Volatility'
            },
            'yaxis': {
                'title': 'Annualised returns'
            }
        }
    }


def get_fixed_ans(fixed='sharpe', value=0.05):
    ret, vol, sharp, weight = optimizer.get_fixed_ans(fixed, value)
    ret = '%.5f' % ret
    vol = '%.5f' % vol
    sharp = '%.5f' % sharp
    return ret, vol, sharp, weight


if __name__ == '__main__':
    data = efficient_frontier_data_layout('all')
    fig = go.Figure(data)
    fig.show()
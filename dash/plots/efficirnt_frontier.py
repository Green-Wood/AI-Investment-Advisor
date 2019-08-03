import plotly.graph_objs as go
from init_optmizer import optimizer
import pathlib
import pandas as pd

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()
instruments = pd.read_csv(DATA_PATH.joinpath('instruments.csv'), usecols=['code', 'symbol', 'fund_type'])


def efficient_frontier_data_layout(id_list):
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
    weight_df = pd.DataFrame.from_dict(weight, orient='index', columns=['weight'])
    weight_df.reset_index(inplace=True)
    weight_df['index'] = weight_df['index'].astype(int)
    weight_df['weight'] = weight_df['weight'].apply(lambda x: '%.5f' % x)
    ins_wei_df = instruments.merge(weight_df, left_on='code', right_on='index')
    ins_wei_df = ins_wei_df.drop(['index'], axis=1)
    return ret, vol, sharp, ins_wei_df

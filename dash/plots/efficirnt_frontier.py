import plotly.graph_objs as go
from init_optmizer import optimizer
import pathlib
import pandas as pd
from PortfolioOptimizer import PortfolioOptimizer
from pypfopt import expected_returns, risk_models
import random

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()
instruments = pd.read_csv(DATA_PATH.joinpath('instruments.csv'), usecols=['code', 'symbol', 'fund_type'])
adjusted_net_value = pd.read_csv(DATA_PATH.joinpath('adjusted_net_value.csv'), index_col=0)

_, _, _, fix_weights = optimizer.get_fixed_ans(fixed='volatility')
fix_random_data = optimizer.get_random_samples(fix_weights)


def get_text_info(data):
    weights = data[3]
    top3_list = [sorted(w.items(), key=lambda x: x[1], reverse=True)[:3] for w in weights]
    basic_info_list = [
        'Returns: {:.3f}%<br>Volatility: {:.3f}%<br>Sharp Ratio: {:.3f}'.format(ret * 100, vol * 100, sr)
        for ret, vol, sr in zip(data[0], data[1], data[2])
    ]
    for i in range(len(basic_info_list)):
        weights = top3_list[i]
        for code, w in weights:
            fund_name = instruments[instruments['code'] == int(code)].iloc[0, 1]
            basic_info_list[i] += '<br>{}: {:.5f}%'.format(fund_name, w * 100)
    return basic_info_list


def efficient_frontier_data_layout(id_list):
    # 模拟用户选择基金
    id_list = list(adjusted_net_value.columns)
    id_list = random.sample(id_list, 20)

    best_frontier = optimizer.efficient_frontier('all')
    vol_list = best_frontier[1] + fix_random_data[1]
    ret_list = best_frontier[0] + fix_random_data[0]
    sharp_ratio_list = best_frontier[2] + fix_random_data[2]
    trace = []
    if id_list is None:
        trace.append(
            go.Scatter(
                x=best_frontier[1],
                y=best_frontier[0],
                opacity=0.75,
                hoverinfo='text',
                text=get_text_info(best_frontier),
                mode='lines',
                line={
                    'color': 'red'
                },
                name='Best recommend'
            )
        )
        trace.append(go.Scatter(
            x=vol_list,
            y=ret_list,
            opacity=0.75,
            hoverinfo='skip',
            mode='markers',
            marker={
                'color': sharp_ratio_list,
                'colorscale': 'Viridis',
            },
            showlegend=False
        ))
    else:
        choose_data_value = adjusted_net_value[id_list]
        op = PortfolioOptimizer(expected_returns.ema_historical_return(choose_data_value),
                                risk_models.CovarianceShrinkage(choose_data_value).ledoit_wolf())
        op.optimize()
        all_risk = op.get_all_ans()[2]
        mid_risk = (all_risk[0] + all_risk[-1]) / 2
        _, _, _, choose_weights = op.get_fixed_ans(fixed='volatility', value=mid_risk)

        choose_data = op.get_random_samples(choose_weights)
        choose_frontier = op.efficient_frontier(id_list)

        best_start = 30 if len(id_list) < 40 else 0
        best_frontier = [x[best_start:] for x in best_frontier]
        trace.append(
            go.Scatter(
                x=best_frontier[1],
                y=best_frontier[0],
                opacity=0.75,
                hoverinfo='text',
                text=get_text_info(best_frontier),
                mode='lines',
                line={
                    'color': 'red'
                },
                name='Best recommend'
            )
        )

        trace.append(go.Scatter(
            x=choose_frontier[1],
            y=choose_frontier[0],
            opacity=0.75,
            hoverinfo='text',
            text=get_text_info(choose_frontier),
            mode='lines',
            line={
                'color': 'green'
            },
            customdata=choose_frontier[3],
            name='Your choice'
        ))
        trace.append(go.Scatter(
            x=choose_data[1],
            y=choose_data[0],
            opacity=0.75,
            hoverinfo='skip',
            mode='markers',
            marker={
                'color': choose_data[2],
                'colorscale': 'Viridis',
            },
            showlegend=False
        ))

    return {
        'data': trace,
        'layout': {
            'legend': {
                'x': -0.01
            },
            'title': {
                'text': 'Efficient Frontier',
            },
            'xaxis': {
                'title': 'Annualised Volatility',
                'tickformat': '%'
            },
            'yaxis': {
                'title': 'Annualised returns',
                'tickformat': '%'
            },
            'hovermode': 'closest'
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

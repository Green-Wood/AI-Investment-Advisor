import plotly.graph_objs as go
from init_optmizer import optimizer


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


def best_sharp_ratio():
    return optimizer.get_fixed_ans()

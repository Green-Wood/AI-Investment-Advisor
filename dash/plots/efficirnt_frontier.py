import plotly.graph_objs as go


def efficient_frontier_data_layout(data):
    """
    list of tuples, [(float, float, float),...,(float,float,float)]
                        Each tuple is (expected return, volatility, Sharpe ratio).
    :param data:
    :return:
    """
    return {
        'data': [
            go.Scatter(
                x=data[1],
                y=data[0],
                opacity=0.75,
                x0=-10,
                text=['Sharpe Ratio: {}'.format(x[2]) for x in data],
                mode='lines',
                line={
                    # 'color': 'rgb(67,67,67)',
                    'width': 3
                }
            ),
        ],
        'layout': go.Layout(

        )
    }

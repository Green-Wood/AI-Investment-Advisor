import plotly.graph_objs as go
import pandas as pd

risk_list = range(12, 48, 6)
df = pd.read_csv(
    'https://raw.githubusercontent.com/plotly/'
    'datasets/master/gapminderDataFiveYear.csv')


def fund_data_layout(risk):
    filtered_df = df[df.year == 1967]
    traces = []
    for i in filtered_df.continent.unique():
        df_by_continent = filtered_df[filtered_df['continent'] == i]
        traces.append(go.Scatter(
            x=df_by_continent['gdpPercap'],
            y=df_by_continent['lifeExp'],
            text=df_by_continent['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))
    return {
        'data': traces,
        'layout': go.Layout(
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            # legend={'x': 0, 'y': 1},
            hovermode='closest',
            clickmode='event+select'
        )
    }

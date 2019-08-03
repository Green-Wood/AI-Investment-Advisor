# coding: utf-8
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
import pathlib


def ploy_sna_pic(codes_list):

    PATH = pathlib.Path(__file__).parent.parent
    DATA_PATH = PATH.joinpath("data").resolve()

    G = nx.Graph()
    # add edge
    if len(codes_list) == 1:
        dict_data = pd.read_csv(DATA_PATH.joinpath('sna_fund_type_manger.csv'), index_col=5, encoding='gb18030')
        edge_data = pd.read_csv(DATA_PATH.joinpath('sna_edge_list.csv'), index_col=0, encoding='gb18030')
        need_data = dict_data.loc[codes_list]
        # node needed
        need_node = []
        for node in need_data['姓名']:
            if not pd.isna(node):
                need_node.append(node)
        # edge needed
        edge_df = edge_data.loc[set(need_node)]
        for i in range(len(edge_df)):
            G.add_edge(edge_df.index[i], edge_df.iloc[i][0])

        # node speace
        node_name = []
        node_fund = []
        node_type = []
        for node in dict_data['姓名']:
            if not pd.isna(node):
                node_name.append(node)
        for node in dict_data['基金名称']:
            if not pd.isna(node):
                node_fund.append(node)
        for node in dict_data['基金类型']:
            if not pd.isna(node):
                node_type.append(node)

        color_list = []
        text_list = []
        for node in G.node():
            if node in node_name:
                color_list.append(1)
                text_name = str(dict_data[dict_data['姓名'] == node].iloc[0]['简介'])
                text_name = text_name.replace('：', '<br>')
                text_name = text_name.replace(':', '<br>')
                text_name = text_name.replace('。', '<br>')
                text_name = text_name.replace('、', '<br>')
                text_name = text_name.replace(';', '<br>')
                text_name = text_name.replace('；', '<br>')
                text_name = text_name.replace('，', '<br>')
                text_name = text_name.replace(',', '<br>')
                text_list.append(text_name)
            if node in node_fund:
                color_list.append(2)
                text_fund = str(dict_data[dict_data['基金名称'] == node].iloc[0][['任职回报', '同类平均', '同类排名']]).split('N')[0]
                text_fund = text_fund.replace('    ', ':')
                text_fund = text_fund.replace('\n', '<br>')
                text_list.append(node + '<br>' + text_fund)
            if node in node_type:
                color_list.append(3)
                text_list.append(node)
    else:
        portfolio_data = pd.read_csv(DATA_PATH.joinpath('sna_portfolio_data.csv'), index_col=0, encoding='gb18030')
        portfolio_data = portfolio_data.loc[codes_list]

        edge_list = []
        for index, row in portfolio_data.iterrows():
            edge_list.append((row['symbol'], row['fund_type'])) # 基金和类型
            if not pd.isna(row['manager_0']):
                edge_list.append((row['fund_type'], row['manager_0']))  # 类型和负责人
                edge_list.append((row['symbol'], row['manager_0']))  # 基金和负责人
                if not pd.isna(row['manager_1']):
                    edge_list.append((row['fund_type'], row['manager_1']))
                    edge_list.append((row['symbol'], row['manager_1']))
                    edge_list.append((row['manager_1'], row['manager_0']))
                    if not pd.isna(row['manager_2']):
                        edge_list.append((row['fund_type'], row['manager_2']))
                        edge_list.append((row['symbol'], row['manager_2']))
                        edge_list.append((row['manager_2'], row['manager_0']))
                        edge_list.append((row['manager_2'], row['manager_1']))
                        if not pd.isna(row['manager_3']):
                            edge_list.append((row['fund_type'], row['manager_3']))
                            edge_list.append((row['symbol'], row[3]))
                            edge_list.append((row['manager_3'], row['manager_0']))
                            edge_list.append((row['manager_3'], row['manager_1']))
                            edge_list.append((row['manager_3'], row['manager_2']))
                            if not pd.isna(row['manager_4']):
                                edge_list.append((row['fund_type'], row['manager_4']))
                                edge_list.append((row['symbol'], row['manager_4']))
                                edge_list.append((row['manager_4'], row['manager_0']))
                                edge_list.append((row['manager_4'], row['manager_1']))
                                edge_list.append((row['manager_4'], row['manager_2']))
                                edge_list.append((row['manager_4'], row['manager_3']))
        edge_set = set(edge_list)
        G.add_edges_from(edge_set)
        # node speace
        node_name = []
        node_fund = []
        node_type = []
        for node in portfolio_data['manager_0']:
            if not pd.isna(node):
                node_name.append(node)
        for node in portfolio_data['manager_1']:
            if not pd.isna(node):
                node_name.append(node)
        for node in portfolio_data['manager_2']:
            if not pd.isna(node):
                node_name.append(node)
        for node in portfolio_data['manager_3']:
            if not pd.isna(node):
                node_name.append(node)
        for node in portfolio_data['manager_4']:
            if not pd.isna(node):
                node_name.append(node)
        for node in portfolio_data['symbol']:
            if not pd.isna(node):
                node_fund.append(node)
        for node in portfolio_data['fund_type']:
            if not pd.isna(node):
                node_type.append(node)

        color_list = []
        for node in G.node():
            if node in node_name:
                color_list.append(1)
            if node in node_fund:
                color_list.append(2)
            if node in node_type:
                color_list.append(3)

    pos = nx.layout.spring_layout(G)  # 布局
    # pos = nx.layout.kamada_kawai_layout(G)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        hoverinfo='none',
        mode='lines')
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)

    if len(codes_list) == 1:
        two_title = '<br>基金经理技能树'
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            text = list(text_list), # 显示的文本信息
            marker=dict(
                colorscale=[[0, 'rgb(242, 162, 89)'], [0.5, 'rgb(244, 102, 101)'], [1.0, 'rgb(79, 142, 235)']],
                color=color_list,
                line_color='rgba(156, 165, 196, 1.0)',
                size=25,  # node大小
                colorbar=dict(
                    tickvals=[1, 2, 3],
                    ticktext=['基金管理人', '基金名称', '基金类型'],
                    thickness=3,
                    # title='Node Information',
                    xanchor='left',
                    titleside='right'
                        ),
                line_width=1))
    else:
        two_title = '<br>基金类别图谱'
        node_trace = go.Scatter(
            x=node_x, y=node_y,
            mode='markers',
            hoverinfo='text',
            text = list(G.node()),  # 显示的文本信息
            marker=dict(
                colorscale=[[0, 'rgb(242, 162, 89)'], [0.5, 'rgb(244, 102, 101)'], [1.0, 'rgb(79, 142, 235)']],

                color=color_list,
                line_color='rgba(156, 165, 196, 0.3)',
                size=15,  # node大小
                colorbar=dict(
                    tickvals=[1, 2, 3],
                    ticktext=['基金管理人', '基金名称', '基金类型'],
                    thickness=3,
                    # title='Node Information',
                    xanchor='left',
                    titleside='right'
                        ),
                line_width=1))

    return {
        'data': [edge_trace, node_trace],
        'layout': go.Layout(
                title=two_title,
                titlefont_size=20,
                showlegend=False,
                hovermode='closest',
                paper_bgcolor='white',
                plot_bgcolor='white',
                margin=dict(b=20, l=5, r=5, t=40),
                annotations=[dict(text="this is text", showarrow=False, xref="paper", yref="paper", x=0.005, y=-0.002 ) ],
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                )
    }


if __name__ == '__main__':

    codes_list = [519661, 61, 398061, 519995, 519095,
                  395, 470059, 259, 59, 519692, 192,
                  166, 100066, 66, 519066, 519666, 257050,
                  510150, 377150, 510650, 510050, 519050,
                  270050, 150, 519150, 310368, 686868,
                  519668, 68, 100068, 519068, 470068, 368,
                  57, 80003, 180003, 550003, 450003, 213003,
                  110003, 630003, 3, 620003, 610103, 161603,
                  519003, 90003, 540003, 630103, 700003]

    plot_s = ploy_sna_pic(codes_list)

    fig = go.Figure(plot_s['data'], plot_s['layout'])
    fig.show()


# coding: utf-8
import plotly.graph_objects as go
import pandas as pd
import networkx as nx
import pathlib


def ploy_sna_pic(codes_list):

    codes_list = [int(x) for x in codes_list]
    PATH = pathlib.Path(__file__).parent.parent
    DATA_PATH = PATH.joinpath("data").resolve()

    G = nx.Graph()
    dict_data = pd.read_csv(DATA_PATH.joinpath('sna_fund_type_manger.csv'), index_col=5, encoding='gb18030')

    # add edge
    if len(codes_list) == 1:

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

    #     pos = nx.layout.spring_layout(G)  # 布局
        pos = nx.layout.kamada_kawai_layout(G)

        node_to_df = []
        for n_i in G.node():
            if n_i in list(dict_data['姓名']):
                text_name = str(dict_data[dict_data['姓名'] == n_i].iloc[0]['简介'])
                text_name = text_name.replace('：', '<br>')
                text_name = text_name.replace(':', '<br>')
                text_name = text_name.replace('。', '<br>')
                text_name = text_name.replace('、', '<br>')
                text_name = text_name.replace(';', '<br>')
                text_name = text_name.replace('；', '<br>')
                text_name = text_name.replace('，', '<br>')
                text_name = text_name.replace(',', '<br>')
                node_to_df.append([n_i, '姓名', text_name, pos[n_i][0], pos[n_i][1]])
            if n_i in list(dict_data['基金名称']):
                text_fund = str(dict_data[dict_data['基金名称'] == n_i].iloc[0][['任职回报', '同类平均', '同类排名']]).split('N')[0]
                text_fund = text_fund.replace('    ',':')
                text_fund = text_fund.replace('\n','<br>')
                node_to_df.append([n_i, '基金名称', n_i + '<br>' + text_fund, pos[n_i][0], pos[n_i][1]])
            if n_i in list(dict_data['基金类型']):
                node_to_df.append([n_i, '基金类型', n_i, pos[n_i][0], pos[n_i][1]])

    else:

        portfolio_data = pd.read_csv(DATA_PATH.joinpath('sna_portfolio_data.csv'), index_col=0, encoding = 'gb18030')
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

    #     pos = nx.layout.spring_layout(G)  # 布局
        pos = nx.layout.kamada_kawai_layout(G)

        node_to_df = []
        for n_i in G.node():
            if n_i in portfolio_data[['manager_0', 'manager_1', 'manager_2', 'manager_3', 'manager_4']].values:
                node_to_df.append([n_i, '姓名',n_i,  pos[n_i][0], pos[n_i][1]])
            if n_i in list(portfolio_data['symbol']):
                fund_inform = dict_data[['任职回报', '同类平均', '同类排名']].loc[4404]
                text_fund = fund_inform[fund_inform['同类平均'] == fund_inform['同类平均'].max()]
                text_fund = str(text_fund.T)
                text_fund = text_fund.replace('\n','<br>')
                node_to_df.append([list(portfolio_data[portfolio_data['symbol'] == n_i].index)[0],'基金名称', n_i + '<br>' + text_fund,  pos[n_i][0], pos[n_i][1]])
            if n_i in list(portfolio_data['fund_type']):
                node_to_df.append([n_i, '基金类型',n_i,  pos[n_i][0], pos[n_i][1]])

    node_df = pd.DataFrame(node_to_df)
    node_df.columns = ['nodes', 'type', 'show_text', 'X', 'Y']

    fig = go.Figure()
    colors = {'姓名':'#e77f67',
                '基金名称':'#778beb',
                '基金类型':'#c23616',
              }
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
    fig.add_trace(go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=1, color='#888'),
        opacity=0.8,
        showlegend=False,
        hoverinfo='none',
        mode='lines'))

    if len(codes_list) == 1:
        titles = '基金经理技能树'
        sizes = 25
    else:
        titles = '基金类别图谱'
        sizes = 18

    for node_i in set(node_df['type'].values):

        fig.add_trace(go.Scatter(
                x = node_df[node_df['type'] == node_i]['X'],
                y = node_df[node_df['type'] == node_i]['Y'],
                name=node_i,
                mode="markers",
                hoverinfo='text',  # 隐藏坐标
                opacity=0.9,
                text = node_df[node_df['type'] == node_i]['show_text'],
                marker=go.scatter.Marker(
                    size=sizes,
                    color=colors[node_i]
                )
            ))

    fig.update_layout(go.Layout(
                    title=titles,
                    titlefont_size=20,
                    plot_bgcolor='white',
                    xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                    yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                 ))

    return fig



if __name__ == "__main__":

    codes_list = [519661, 61, 398061, 519995, 519095,
                  395, 470059, 259, 59, 519692, 192,
                  166, 100066, 66, 519066, 519666, 257050,
                  510150, 377150, 510650, 510050, 519050,
                  270050, 150, 519150, 310368, 686868,
                  519668, 68, 100068, 519068, 470068, 368,
                  57, 80003, 180003, 550003, 450003, 213003,
                  110003, 630003, 3, 620003, 610103, 161603,
                  519003, 90003, 540003, 630103, 700003]

    fig = ploy_sna_pic(codes_list)
    fig.show()

import plotly.graph_objects as go
import pandas as pd


# todo: instruments.csv文件调用
def radar_type(df: dict):
    """
    :param df:dict（多只）基金代码:该基金权重
    :return:data_list: dict  基金类型:该类型占比
    """
    # 此处路径应为instruments.csv的路径，注意编码
    # data = pd.read_csv('Data/instruments.csv',encoding='utf-8')
    try:
        data = pd.read_csv('../../Data/instruments_ansi.csv',encoding='ANSI')
    except:
        print('Error!:instruments.csv的路径错误，请核对')
        return ''
    data_list = {'Hybrid':0,
                 'Bond':0,
                 'Stock':0,
                 'QDII':0,
                 'Money':0
                  }
    for key in df.keys():
        idx = list(data['code']).index(int(key))
        a_type = data['fund_type'][idx]
        if a_type in data_list.keys():
            data_list[a_type] = data_list[a_type] + df[key]
        else:
            print("Warning:This type is not in type_list")

    return data_list


if __name__ == '__main__':
    # test demo
    # 注意需要Data/instruments_ansi.csv
    data = {'000001':0.5,
            '000003':0.3,
            '000007':0.2,
            '000008':0.1,
            }
    w_list = radar_type(data)
    print(w_list)

    # 画雷达图
    fig = go.Figure(data=go.Scatterpolar(
        r=list(w_list.values()),
        theta=list(w_list.keys()),
        fill='toself'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True
            ),
        ),
        showlegend=False
    )
    fig.show()

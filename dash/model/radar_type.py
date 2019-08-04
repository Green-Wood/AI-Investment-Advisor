import plotly.graph_objects as go
import pandas as pd


def get_w(dic: dict):
    """
    :param dic:dict（多只）基金代码:该基金权重
    :return:data_dic: dict  基金类型:该类型占比
    """
    # 此处路径应为instruments.csv的路径，注意编码
    # data = pd.read_csv('Data/instruments.csv',encoding='utf-8')
    try:
        data = pd.read_csv('../Data/instruments.csv')
    except:
        print('Error!:instruments.csv的路径错误，请核对')
        return ''
    data_dic = {
                'Hybrid': 0,
                'Bond': 0,
                'Stock': 0,
                'QDII': 0,
                'Money': 0,
                'Related': 0,
                'Other': 0
    }
    for key in dic.keys():
        idx = list(data['code']).index(int(key))
        a_type = data['fund_type'][idx]
        if a_type in data_dic.keys():
            data_dic[a_type] = data_dic[a_type] + dic[key]
        else:
            print("Warning:This type is not in type_list")
    sum = 0
    for key in data_dic.keys():
        sum = sum + data_dic[key]
    for key in data_dic.keys():
        data_dic[key] = data_dic[key]/sum
    return data_dic


def radar_type(dic: dict):
    """
    :param df:  df:dict （多只）基金代码:该基金权重
    :return:   dict : {
                        'data':go.Figure.data ,
                        'layout':go.Figure.layout
                    }
    """
    w_dic = get_w(dic)
    fig = go.Figure(data=go.Scatterpolar(
                r=list(w_dic.values()),
                theta=list(w_dic.keys()),
                fill='toself'
    ))
    return {
            'data':fig.data,
            'layout':fig.layout
    }


if __name__ == '__main__':
    # test demo
    # 注意需要Data/instruments_ansi.csv
    data = {'000001':0.5,
            '000003':0.3,
            '000007':0.2,
            '000028':0.1,
            '960001':0.3
            }
    dic = radar_type(data)
    print(dic)

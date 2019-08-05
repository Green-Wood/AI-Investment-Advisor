from plotly.subplots import make_subplots
import plotly.graph_objects as go
import pandas as pd
import numpy as np


#  todo:instruments.csv
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
    data_dic = {'Hybrid': 1e-28 ,
                'Bond': 1e-28,
                'Stock': 1e-28,
                'QDII': 1e-28,
                'Money': 1e-28,
                'Related': 1e-28,
                'Other': 1e-28
                }
    for key in dic.keys():
        idx = list(data['code']).index(int(key))
        a_type = data['fund_type'][idx]
        if a_type in data_dic.keys():
            data_dic[a_type] = data_dic[a_type] + dic[key]
        else:
            print("Warning:This type is not in type_list {}".format(a_type))

    # log
    for key in data_dic.keys():
        data_dic[key] = np.log10(data_dic[key])
    val_max = np.max(list(data_dic.values()))
    val_min = np.min(list(data_dic.values()))
    for key in data_dic.keys():
        data_dic[key] = (data_dic[key]-val_min)/(val_max-val_min)
    return data_dic


def show_barpolar(dic: dict):
    w_dic = get_w(dic)
    # print(w_dic)
    fig = make_subplots(
        rows=1,cols=1,
        column_titles=['类型分布图'],
        specs=[[{"type": "barpolar"}]]
    )

    fig.add_trace(go.Barpolar(
                theta=list(w_dic.keys()),
                r=list(w_dic.values()),),
                row=1,col=1
        )
    # fig.show()
    return {
        'data': fig.data,
        'layout':fig.layout
    }


if __name__ == '__main__':
    data = {'100066': 0.019697766323527984, '100068': 0.01842395122855841, '159934': 7.129683948522186e-10, '160128': 2.564896083103935e-10, '160129': 1.5417479777515332e-10, '160719': 0.0031517793846117872, '161117': 3.6018968859157724e-08, '161119': 1.5002288540100555e-10, '161603': 3.4203674248081214e-11, '161614': 5.616907432154107e-11, '161618': 3.955442897531186e-11, '161619': 3.955460634648427e-11, '161911': 2.3715556655292384e-10, '163210': 1.6268360657699485e-10, '163211': 1.20572830966065e-10, '166902': 2.409155472055478e-09, '166903': 7.150069994355632e-10, '166904': 0.0046755167352753035, '320021': 1.7714610660824343e-11, '518800': 6.549120357466134e-10, '518880': 5.17103351205782e-10, '519023': 0.006339421597626161, '519024': 0.007617244800924412, '519152': 0.05662516432788167, '519153': 0.06315041975805015, '519662': 0.001605436369947905, '519669': 4.741656727594895e-10, '519723': 8.026051100557229e-10, '519725': 2.057748628510866e-08, '650001': 0.0016396582441241757, '650002': 4.926742996442935e-07, '000129': 0.057909239366958055, '000216': 2.9360313684823825e-08, '000187': 5.93325795863459e-10, '000217': 0.0034171484393386163, '040026': 0.02634364907566826, '000286': 0.007348206325350952, '000186': 5.560141130413768e-11, '000188': 3.1926797957813145e-10, '070009': 0.1187968407810713, '000191': 5.2934685997464364e-11, '000396': 0.03420542354877045, '040046': 8.815689068389671e-11, '000346': 0.056847470431375446, '040041': 0.02871292771591631, '000148': 8.907209870162577e-11, '000084': 0.06458316572196884, '040040': 0.02629916147005846, '000347': 0.049575371899222835}
    dic = show_barpolar(data)

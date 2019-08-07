import plotly.figure_factory as ff
import numpy as np
import pandas as pd


# todo: 字体大小 fig.layout.annotations[i].font.size
def plot_heatmap(df: pd.DataFrame):
    """
    :param (DataFrame) df:协方差矩阵
    :return: (dict) fig{
                    'data':
                    'layout':
            }
    """
    codes = df.columns.values
    z = df.as_matrix()
    zmin = np.min(z)
    # 保留两位数作为文本显示
    z2 = np.around(z,decimals=2)
    z_text=[]
    # 变为下三角矩阵
    for i in range(len(z)):
        z_text.append([])
        for j in range(len(z[i])):
            if j<(i+1):
                z_text[i].append(str(z2[i,j]))
            else:
                z_text[i].append('')
                z[i,j] = zmin
    # customdatas  两个对应基金号,以空格隔开,格式为 'code code'
    customdatas = []
    for i in range(len(z)):
        customdatas.append([])
        customdatas[i] = [(str(codes[i]) + ' ' + str(codes[j])) for j in range(len(z[i]))]
    fig = ff.create_annotated_heatmap(z,
                                      annotation_text=z_text,
                                      colorscale='Greys',
                                      showscale=True,
                                      hoverinfo='all',
                                      customdata=customdatas
    )
    # 变换字体大小
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 8
    # fig.show()
    return {
        'data': fig.data,
        'layout': fig.layout
    }


if __name__ == '__main__':
    # test demo
    z = np.random.randn(20, 20)
    fig = plot_heatmap(pd.DataFrame(z))
    print(fig)
    a = fig['data'][0].customdata



import pandas as pd
from pypfopt import risk_models
import numpy as np
import pathlib

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()
path_adjusted_net_value = DATA_PATH.joinpath('adjusted_net_value.csv')
path_instruments = DATA_PATH.joinpath('instruments.csv')


def get_corr(code_list: list = None, adjusted_df: pd.DataFrame = None):
    """
    note： 参数二选一
    :param (list) code_list: 基金列表
    :param (DataFrame) adjusted_df: 净值信息
    :return: (DataFrame) corr_df: 协方差矩阵
    eg:     codes = ['257050', '000395', '000001', '519050']
            corr = get_corr(codes)
            print(corr)
    """
    instruments_df = pd.read_csv(path_instruments)

    if code_list is None:
        pass
    if adjusted_df is None:
        adjusted_df = pd.read_csv(path_adjusted_net_value)[code_list]
    # 建立索引
    new_index = []
    for code in adjusted_df.columns.values:
        new_index.append(instruments_df['symbol'][instruments_df['code'].isin([code])].values[0])
    cov = risk_models.CovarianceShrinkage(adjusted_df).ledoit_wolf()
    var = np.eye(cov.shape[0]) * cov
    std = np.power(var, 0.5)
    I = np.linalg.inv(std)
    corr = I.dot(cov).dot(I)
    corr_df = pd.DataFrame(corr, columns=new_index, index=new_index)
    return corr_df


if __name__ == '__main__':
    codes = ['257050','000395','000001','519050']
    corr = get_corr(codes)
    print(corr)
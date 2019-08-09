from PortfolioOptimizer import PortfolioOptimizer
from pypfopt import expected_returns, risk_models
import pathlib
import pandas as pd

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()
adjusted_net_value = pd.read_csv(DATA_PATH.joinpath('adjusted_net_value.csv'))


def get_optimizer_by_list(id_list):
    """
    根据基金代码列表，获得一个优化器
    :param id_list:
    :return:
    """
    choose_data_value = adjusted_net_value[id_list]
    op = PortfolioOptimizer(expected_returns.ema_historical_return(choose_data_value),
                            risk_models.CovarianceShrinkage(choose_data_value).ledoit_wolf())
    op.optimize()
    return op

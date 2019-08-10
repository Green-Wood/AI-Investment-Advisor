

import pandas as pd
import numpy as np
from PortfolioOptimizer import PortfolioOptimizer
import pypfopt.expected_returns as expected_returns
import pypfopt.risk_models as risk_models
import datetime


def get_weights(data,start_date,end_date,columns,fixed='sharpe',value=0.05):
    """

    :param data: DataFrame,
        Full data without missing values, columns are identifiers
        for different data, index is datetime.
    :param start_date: str
        Start date to estimate mu and sigma.
    :param end_date: str
        End date to estimate mu and sigma.
    :param columns: list, ['id1', 'id2',..., 'idn']
        Identifiers of data to use to optimize.
    :param fixed: str, 'sharpe' or 'volatility' or 'return'
        Optimization constraints, defaults to 'sharpe'.
    :param value: float
        Optimization constraints. No need to set if fixed is
        'sharpe', defaults to 0.05.
    :return: tuple, (float, float, float, dict)
        The closest answer given fixed constraints.
        (return, volatility, Sharpe ratio, weights)
        weights == {'id1':w1, 'id2':w2, ..., 'idn':wn}
    """
    while start_date not in data.index:
        splits=start_date.split('-')
        y,m,d=int(splits[0]),int(splits[1]),int(splits[2])
        start_date=(datetime.datetime(y, m, d) + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    while end_date not in data.index:
        splits=end_date.split('-')
        y,m,d=int(splits[0]),int(splits[1]),int(splits[2])
        end_date=(datetime.datetime(y, m, d) + datetime.timedelta(days=-1)).strftime('%Y-%m-%d')

    # print(start_date)
    # print(end_date)
    subdata=data.loc[start_date:end_date,columns]
    optimizer=PortfolioOptimizer(expected_returns.ema_historical_return(subdata),
                                 risk_models.CovarianceShrinkage(subdata).ledoit_wolf())
    optimizer.optimize(N=20)
    return optimizer.get_fixed_ans(fixed,value)


#if __name__ == '__main__':
#    with open(r"adjusted_net_value.csv",'r') as f:
#        data = pd.read_csv( f,
#                           index_col=0)
#
#    _,_,_,weights = get_weights(data, '2014-01-04', '2014-01-12',
#                     columns=['590002', '610002', '620002', '630002'],
#                     fixed='sharpe')
#
#    print(get_weights(data, '2014-01-04', '2014-01-12',
#                     columns=['590002', '610002', '620002', '630002'],
#                     fixed='volatility',
#                     value=0.05))
#
#    print(get_weights(data,'2014-01-04','2014-01-12',
#                columns=['590002','610002','620002','630002'],
#                fixed='return',
#                value=0.05))





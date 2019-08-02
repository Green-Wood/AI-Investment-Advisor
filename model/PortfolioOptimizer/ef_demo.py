from PortfolioOptimizer import PortfolioOptimizer
from pypfopt.efficient_frontier import EfficientFrontier
import pypfopt.expected_returns as expected_returns
import pypfopt.risk_models as risk_models
import pandas as pd
import matplotlib.pyplot as plt
from time import time
import pickle

if __name__ == '__main__':
    data = pd.read_csv('C:/Users/qin_t/Desktop/PortfolioOptimization/funds/funds/adjusted_net_value.csv',
                       index_col=0)

    print('Loading from file...')
    f = open('optimizer', 'rb')
    optimizer = pickle.load(f)
    print('Done.')

    # optimizer = PortfolioOptimizer(data,
    #                                expected_returns.ema_historical_return(data),
    #                                risk_models.CovarianceShrinkage(data).ledoit_wolf(),
    #                                risk_free_rate=0.02)
    # start=time()
    # print('-'*80)
    # print('Optimizing...')
    # optimizer.optimize(N=100)
    # end=time()
    # print('Done. Time cost = '+str(end-start))

    print('-' * 80)
    print("Maximum Sharpe ratio:")
    ret, risk, sharpe, weights = optimizer.get_fixed_ans(fixed='sharpe')
    print("return = {}, risk = {}, sharpe = {}".format(ret, risk, sharpe))
    print('-' * 80)
    print("Fixed risk = 0.05:")
    ret, risk, sharpe, weights = optimizer.get_fixed_ans(fixed='volatility', value=0.05)
    print("return = {}, risk = {}, sharpe = {}".format(ret, risk, sharpe))

    print('-' * 80)
    print("Fixed return = 0.15:")
    ret, risk, sharpe, weights = optimizer.get_fixed_ans(fixed='return', value=0.15)
    print("return = {}, risk = {}, sharpe = {}".format(ret, risk, sharpe))

    print('-' * 80)
    print("Plotting efficient frontier of all funds...")
    returns, risks, sharpes, weights_list = optimizer.efficient_frontier(columns='all', risk_free_rate=0.02)
    plt.figure(1)
    plt.plot(risks, returns)

    print('-' * 80)
    print("Plotting efficient frontier of funds with weight > 1e-10...")
    columns = [key for key, v in weights.items() if v > 1e-10]
    print("number of funds with weight > 1e-10 is " + str(len(columns)))
    returns, risks, sharpes, weights_list = optimizer.efficient_frontier(columns=columns, risk_free_rate=0.02)
    plt.figure(2)
    plt.plot(risks, returns)

    plt.show()

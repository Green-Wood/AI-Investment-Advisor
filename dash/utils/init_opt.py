import pandas as pd
from model.PortfolioOptimizer import PortfolioOptimizer
from pypfopt import expected_returns
from pypfopt import risk_models

data = pd.read_csv('data/adjusted_net_value.csv', index_col=0)


optimizer = PortfolioOptimizer(data,
                               expected_returns.ema_historical_return(data),
                               risk_models.CovarianceShrinkage(data).ledoit_wolf())

ret = optimizer.optimize()
print(ret)
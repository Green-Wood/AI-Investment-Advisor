import pathlib
import pandas as pd
from time import time
from model.backtesting import get_performance
from datetime import datetime

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()


def get_best_portfolio():
    pass


def get_portfolio_data(codes):
    with open(DATA_PATH.joinpath('date.csv')) as f:
        start_end = pd.read_csv(f, index_col=0)
    with open(DATA_PATH.joinpath('adjusted_net_value.csv')) as f:
        nav = pd.read_csv(f, index_col=0)
    if codes == 'all':
        codes = nav.columns
    print("Getting portfolio backtest results...")

    start = time()
    data = get_performance(nav, start_end, codes, fixed='sharpe')
    print("Done: %.2fs elapsed" % (time() - start))

    # index_df = pd.DataFrame(index=["Annu. return", "Alpha", "Win Rate",
    #                                "Max drawdown", "Sharpe Ratio", "Sortino Ratio"])
    # for k, v in results.items():
    #     index_df[k] = parse_info(v)
    return data['return_p'].index.to_pydatetime(), data['return_p'].values, \
           data['return_b'].index.to_pydatetime(), data['return_b'].values, data['index']


def get_single_fund_data(code):
    df0 = pd.read_csv(DATA_PATH.joinpath("adjusted_net_value.csv"), parse_dates=["datetime"], index_col=0)
    upper = pd.read_csv(DATA_PATH.joinpath("yhat_upper_total.csv"))
    lower = pd.read_csv(DATA_PATH.joinpath("yhat_lower_total.csv"))
    df1 = pd.read_csv(DATA_PATH.joinpath("yhat_total.csv"), parse_dates=["datetime"])
    forecast_time = df1['datetime']
    df0 = df0.loc['2017-01-01':'2018-12-11']
    history = df0[code]
    last = history[-1:]
    his_x, his_y = df0.index, history
    forecast_x, forecast_y = forecast_time, pd.concat((last, df1[code]))
    upper_y = pd.concat((last, upper[code]))
    lower_y = pd.concat((last, lower[code]))
    return his_x.to_pydatetime(), his_y.values, forecast_x, lower_y.values, \
           forecast_y.values, upper_y.values


if __name__ == '__main__':
    # p, b, index = get_portfolio_data(['000059', '000395'])
    # p.to_csv(DATA_PATH.joinpath('best_portfolio.csv'))
    # b.to_csv(DATA_PATH.joinpath('baseline.csv'))
    # print(index)

    his_x, his_y, forecast_x, lower_y, forecast_y, upper_y = get_single_fund_data('000059')
    print(his_x)

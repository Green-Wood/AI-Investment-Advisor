import pathlib
import pandas as pd
from time import time
from model.backtesting import get_performance
from datetime import datetime
from init_optmizer import optimizer
import json

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()

df0 = pd.read_csv(DATA_PATH.joinpath("adjusted_net_value.csv"), parse_dates=["datetime"], index_col=0)
upper = pd.read_csv(DATA_PATH.joinpath("yhat_upper_total.csv"))
lower = pd.read_csv(DATA_PATH.joinpath("yhat_lower_total.csv"))
df1 = pd.read_csv(DATA_PATH.joinpath("yhat_total.csv"), parse_dates=["datetime"])

start_end = pd.read_csv(DATA_PATH.joinpath('date.csv'), index_col=0)
nav = pd.read_csv(DATA_PATH.joinpath('adjusted_net_value.csv'), index_col=0)

best_portfolio = pd.read_csv(DATA_PATH.joinpath('best_portfolio.csv'))
with open(DATA_PATH.joinpath('info.txt'), 'r') as json_file:
    best_portfolio_info = json.load(json_file)


def get_portfolio_data(codes):
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
    return data['return_p'].index.to_pydatetime(), data['return_p'].values, data['return_b'].values, data['index']


def get_single_fund_data(code):
    forecast_time = df1['datetime']
    small_df0 = df0.loc['2017-01-01':'2018-12-11']
    history = small_df0[code]
    last = history[-1:]
    his_x, his_y = small_df0.index, history
    forecast_x, forecast_y = forecast_time, pd.concat((last, df1[code]))
    upper_y = pd.concat((last, upper[code]))
    lower_y = pd.concat((last, lower[code]))
    return his_x.to_pydatetime(), his_y.values, forecast_x, lower_y.values, \
           forecast_y.values, upper_y.values


if __name__ == '__main__':
    risk_list = [0.01, 0.02, 0.03, 0.04, 0.05]
    df_list = []
    info = dict()
    for risk in risk_list:
        _, _, _, weight = optimizer.get_fixed_ans('volatility', risk)
        fund_list = [k for k, v in weight.items() if v > 1e-7]
        p, b, index = get_portfolio_data(fund_list)
        internal_df = pd.concat([p, b], axis=1)
        internal_df.columns = ['portfolio_{}'.format(risk), 'baseline_{}'.format(risk)]
        df_list.append(internal_df)
        info[risk] = index

    risk_df = pd.concat(df_list, axis=1)
    risk_df.to_csv(DATA_PATH.joinpath('best_portfolio.csv'))
    with open(DATA_PATH.joinpath('info.txt'), 'w') as json_file:
        json.dump(info, json_file)



    # p.to_csv(DATA_PATH.joinpath('best_portfolio.csv'))
    # b.to_csv(DATA_PATH.joinpath('baseline.csv'))
    # print(index)
    #
    # his_x, his_y, forecast_x, lower_y, forecast_y, upper_y = get_single_fund_data('000059')
    # print(his_x)

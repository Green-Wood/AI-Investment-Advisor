# -*- coding: utf-8 -*-


import pandas as pd
import numpy as np
from datetime import datetime
from model.tools import get_weights
from model.performance_pybt import performance_summary
from time import time
import json
from init_optmizer import optimizer


def get_weights_mtx(nav, start_end, fund_cols, fixed='sharpe', nav_predict=None):
    # fixed: 'sharpe' or 'volatility' or 'return'
    W = []

    for i in range(len(start_end.values)):

        v = start_end.values[i]
        s, e = v[0], v[1]

        if type(nav_predict) == type(None):

            _, _, _, weights = get_weights(nav, s, e,
                                           columns=fund_cols,
                                           fixed=fixed)

        else:
            if i < len(start_end.values) - 1:
                e_2 = start_end.values[i + 1][1]
            else:
                e_2 = e
            nav_pre = pd.concat([nav.loc[:e], nav_predict.loc[e:]], axis=0, sort=True)

            _, _, _, weights = get_weights(nav_pre, s, e_2,
                                           columns=fund_cols,
                                           fixed=fixed)

        W.append(np.array(list(weights.values())))

    W = pd.DataFrame(W, columns=fund_cols, index=start_end['end'])

    return W


def get_fund_type_weight(instruments, fund_cols):
    instruments_sel = instruments.loc[fund_cols]

    fund_type_weight = instruments_sel['fund_type'].value_counts()

    return fund_type_weight / fund_type_weight.sum()


def get_nav_series(nav, start_end, fund_cols, fixed='sharpe', w_flag=1, prc_date=None, nav_predict=None):
    nav.index = pd.to_datetime(nav.index)

    end = start_end['end']

    if w_flag == 1:  # markowitz
        W = get_weights_mtx(nav, start_end, fund_cols, fixed=fixed, nav_predict=nav_predict)
    elif w_flag == 0:  # equal allocation
        eql = [[1 / len(fund_cols) for ix in range(len(fund_cols))] for i in range(len(end))]
        W = pd.DataFrame(eql, columns=fund_cols, index=end)

    if type(prc_date) == type(None):
        nav_sel = nav[fund_cols]
    else:
        nav_sel = nav.loc[prc_date:][fund_cols]

    end_val = 1
    VAL = pd.DataFrame(columns=fund_cols)

    for i in range(len(end)):
        e = end.iloc[i]

        if i == len(end) - 1:
            ohlc = nav_sel.loc[e:]
        else:
            ohlc = nav_sel.loc[e:end.iloc[i + 1]]

        w = W[fund_cols].loc[e]

        scaler = (ohlc.iloc[0] * w).sum()
        w_scl = w * end_val / scaler

        val = ohlc.mul(w_scl, axis=1)
        VAL = pd.concat([VAL, val.iloc[:-1]])

        end_val = val.iloc[-1].sum()

    return VAL.sum(axis=1)


def get_performance(nav, instruments, index, start_end, fund_cols, fixed='sharpe', prc_date=None, nav_predict=None):
    end = start_end['end']

    NAV = get_nav_series(nav, start_end, fund_cols, fixed=fixed, w_flag=1, prc_date=prc_date,
                         nav_predict=nav_predict)

    eqd = NAV.pct_change()  # daily return

    eqd_t = (NAV - NAV.iloc[0]) / NAV.iloc[0]  # total return

    w_index = get_fund_type_weight(instruments, fund_cols).reindex(index.columns).fillna(0)

    eqd_bl = index.mul(w_index, axis=1).sum(1)

    eqd_bl_t = eqd_bl.cumsum()

    perf_all = performance_summary(eqd, eqd_bl)

    d = {'return_p': eqd_t, 'return_b': eqd_bl_t}
    d.update({'all': perf_all})

    return d


def get_data(codes):
    with open('../data/date.csv') as f:
        traday = pd.read_csv(f)
        # h = lambda x: datetime.strftime(datetime.strptime(x, "%Y/%d/%m"), "%Y-%d-%m")
        start = traday['start']
        end = traday['end']
        start_end = pd.concat([start, end], axis=1)

    with open('../data/adjusted_net_value.csv') as f:
        nav = pd.read_csv(f, index_col=0)

    with open('2016-2018_voting_2.csv', 'r') as f:
        voting_2 = pd.read_csv(f, index_col=0)
        voting_2.columns = voting_2.columns.map(lambda x: str(int(x)).zfill(6))
        voting_2.index = pd.to_datetime(voting_2.index)

    with open('instruments_ansi.csv', 'rb') as f:
        instruments = pd.read_csv(f, index_col=0, encoding='gbk')
        instruments['code'] = instruments['code'].map(lambda x: str(x).zfill(6))
        instruments.set_index('code', inplace=True)

    with open('index.csv', 'r') as f:
        index = pd.read_csv(f, index_col=0)
        index.index = index.index.map(lambda x: datetime.strptime(x, "%Y/%m/%d"))
        index = index.loc[end.iloc[12]:]

    fund_cols = nav.columns

    print("Getting portfolio backtest results...")

    start = time()
    d = get_performance(nav, instruments, index, start_end.iloc[12:], codes, fixed='sharpe',
                        prc_date='20160101', nav_predict=voting_2)

    print("Done: %.2fs elapsed" % (time() - start))

    return d['return_p'], d['return_b'], d['all']


if __name__ == '__main__':
    risk_list = [0.01, 0.02, 0.03, 0.04, 0.05]
    df_list = []
    info = dict()
    for risk in risk_list:
        _, _, _, weight = optimizer.get_fixed_ans('volatility', risk)
        fund_list = [k for k, v in weight.items() if v > 1e-7]
        p, b, index = get_data(fund_list)
        internal_df = pd.concat([p, b], axis=1)
        internal_df.columns = ['portfolio_{}'.format(risk), 'baseline_{}'.format(risk)]
        df_list.append(internal_df)
        info[risk] = index

    risk_df = pd.concat(df_list, axis=1)
    risk_df.to_csv('best_portfolio.csv')
    with open('info.txt', 'w') as json_file:
        json.dump(info, json_file)

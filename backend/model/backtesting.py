# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from model import performance_pybt
from model.tools import get_weights

import pathlib


# 计算每个时间点的基金权重
def get_weights_mtx(nav, start_end, fund_cols, fixed='sharpe'):
    # fixed: 'sharpe' or 'volatility' or 'return'
    W = []
    for v in start_end.values:
        s, e = v[0], v[1]
        _, _, _, weights = get_weights(nav, s, e,
                                       columns=fund_cols,
                                       fixed=fixed)

        W.append(np.array(list(weights.values())))

    W = pd.DataFrame(W, columns=fund_cols, index=start_end['end'])

    return W


# print(get_weights_mtx(nav, start_end, fund_cols, fixed = 'sharpe'))


# 净值

def get_nav_series(nav, start_end, fund_cols, fixed='sharpe', w_flag=1):
    nav.index = pd.to_datetime(nav.index)
    start_end.index = pd.to_datetime(start_end.index)

    end = start_end['end']

    if w_flag == 1:  # markowitz
        W = get_weights_mtx(nav, start_end, fund_cols, fixed=fixed)
    elif w_flag == 0:  # equal allocation
        eql = [[1 / len(fund_cols) for ix in range(len(fund_cols))] for i in range(len(end))]
        W = pd.DataFrame(eql, columns=fund_cols, index=end)

    nav_sel = nav[fund_cols]
    end_val = 1
    VAL = pd.DataFrame(columns=fund_cols)

    for i in range(len(end)):
        e = end[i]

        if i == len(end) - 1:
            ohlc = nav_sel.loc[e:]
        else:
            ohlc = nav_sel.loc[e:end[i + 1]]

        w = W[fund_cols].loc[e]

        scaler = (ohlc.iloc[0] * w).sum()
        w_scl = w * end_val / scaler

        val = ohlc.mul(w_scl, axis=1)
        VAL = pd.concat([VAL, val.iloc[:-1]])

        end_val = val.iloc[-1].sum()

    return VAL.sum(axis=1)


# print(get_nav_series(nav, start_end, fund_cols, fixed = 'sharpe'))


def get_performance(nav, start_end, fund_cols, fixed='sharpe'):
    end = start_end['end']

    NAV = get_nav_series(nav, start_end, fund_cols, fixed, w_flag=1)

    NAV_bl = get_nav_series(nav, start_end, fund_cols, fixed, w_flag=0)

    eqd = NAV.pct_change()  # daily return

    eqd_bl = NAV_bl.pct_change()

    eqd_t = (NAV - NAV.iloc[0]) / NAV.iloc[0]  # total return

    eqd_t_bl = (NAV_bl - NAV_bl.iloc[0]) / NAV_bl.iloc[0]

    perf_all = performance_pybt.performance_summary(eqd, eqd_bl)
    dt_1m = end.iloc[-1]
    perf_1m = performance_pybt.performance_summary(eqd[dt_1m:], eqd_bl[dt_1m:])
    dt_3m = end.iloc[-3]
    perf_3m = performance_pybt.performance_summary(eqd[dt_3m:], eqd_bl[dt_3m:])
    dt_6m = end.iloc[-6]
    perf_6m = performance_pybt.performance_summary(eqd[dt_6m:], eqd_bl[dt_6m:])
    dt_1y = end.iloc[-12]
    perf_1y = performance_pybt.performance_summary(eqd[dt_1y:], eqd_bl[dt_1y:])
    dt_ys = end.iloc[36]
    perf_ys = performance_pybt.performance_summary(eqd[dt_ys:], eqd_bl[dt_ys:])

    d = {'return_p': eqd_t, 'return_b': eqd_t_bl, 'index': {}}
    d['index'].update({'all': perf_all})
    d['index'].update({"1": perf_1m})
    d['index'].update({"3": perf_3m})
    d['index'].update({"6": perf_6m})
    d['index'].update({"12": perf_1y})
    d['index'].update({'ytd': perf_ys})

    return d

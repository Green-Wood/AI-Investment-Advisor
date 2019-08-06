# coding: utf8

# part of pybacktest package: https://github.com/ematvey/pybacktest

""" Functions for calculating performance statistics and reporting """

import pandas as pd
import numpy as np
from datetime import datetime 


start = lambda eqd: eqd.index[0]
end = lambda eqd: eqd.index[-1]
days = lambda eqd: (eqd.index[-1] - eqd.index[0]).days

trades_per_month = lambda eqd: eqd.groupby(
    lambda x: (x.year, x.month)
).apply(lambda x: x[x != 0].count()).mean()
profit = lambda eqd: eqd.sum()   

average = lambda eqd: eqd[eqd != 0].mean()
average_gain = lambda eqd: eqd[eqd > 0].mean() 
average_loss = lambda eqd: eqd[eqd < 0].mean() 

winrate = lambda eqd: float(sum(eqd > 0)) / len(eqd)
payoff = lambda eqd: eqd[eqd > 0].mean() / -eqd[eqd < 0].mean()     
pf = PF = lambda eqd: abs(eqd[eqd > 0].sum() / eqd[eqd < 0].sum())
maxdd = lambda eqd: (eqd.cumsum().expanding().max() - eqd.cumsum()).max()
rf = RF = lambda eqd: eqd.sum() / maxdd(eqd)
trades = lambda eqd: len(eqd[eqd != 0])
_days = lambda eqd: eqd.resample('D').sum().dropna()


def profit_yy(eqd):
    ''' yearly return'''
    d = _days(eqd)
    return d.mean() * 252

def beta(eqd, bl):
    d = _days(eqd)
    b = _days(bl)
    return d.cov(b) / b.var()
  
def alpha(eqd, bl):
    d = _days(eqd)
    b = _days(bl)
    return profit_yy(d) - beta(eqd, bl)*profit_yy(b) 

def ir(eqd, bl):
    ''' information ratio '''
    d = _days(eqd)
    b = _days(bl)
    return ((d.mean()-b.mean()) / (d-b).std()) * (252**0.5)

def calmar(eqd):
    ''' calmar ratio '''
    d = _days(eqd)
    return (d.mean() / maxdd(eqd)) * (252)


def sharpe(eqd):
    ''' daily sharpe ratio '''
    d = _days(eqd)
    return (d.mean() / d.std()) * (252**0.5)


def sortino(eqd):
    ''' daily sortino ratio '''
    d = _days(eqd)
    return (d.mean() / d[d < 0].std()) * (252**0.5)


def ulcer(eqd):
    eq = eqd.cumsum()
    return (((eq - eq.expanding().max()) ** 2).sum() / len(eq)) ** 0.5


def upi(eqd, risk_free=0):
    eq = eqd[eqd != 0]
    return (eq.mean() - risk_free) / ulcer(eq)
UPI = upi


def mpi(eqd):
    """ Modified UPI, with enumerator resampled to months (to be able to
    compare short- to medium-term strategies with different trade frequencies. """
    return eqd.resample('M').sum().mean() / ulcer(eqd)
MPI = mpi


def mcmdd(eqd, runs=100, quantile=0.99, array=False):
    maxdds = [maxdd(eqd.take(np.random.permutation(len(eqd)))) for i in range(runs)]
    if not array:
        return pd.Series(maxdds).quantile(quantile)
    else:
        return maxdds




def performance_summary(equity_diffs, benchmark_diffs, quantile=0.99, precision=4):
    def _format_out(v, precision=4):
        if isinstance(v, dict):
            return {k: _format_out(v) for k, v in list(v.items())}
        if isinstance(v, (float, np.float)):
            v = round(v, precision)
        if isinstance(v, np.generic):
            return np.asscalar(v)
        return v

    def force_quantile(series, q):
        return sorted(series.values)[int(len(series) * q)]

    eqd = equity_diffs[equity_diffs != 0]
    
    bl = benchmark_diffs[benchmark_diffs != 0]
    
    if getattr(eqd.index, 'tz', None) is not None:
        eqd = eqd.tz_convert(None)
    if len(eqd) == 0:
        return {}
#    hold = holding_periods(equity_diffs)

#    return _format_out({
#        'backtest': {
#            'from': str(start(eqd)),
#            'to': str(end(eqd)),
#            'days': days(eqd),
#            'trades': len(eqd),
#            },
#        'performance': {
#            'profit': eqd.sum(),
#            'averages': {
#                'trade': average(eqd),
#                'gain': average_gain(eqd),
#                'loss': average_loss(eqd),
#                },
#            'winrate': winrate(eqd),
#            'payoff': payoff(eqd),
#            'PF': PF(eqd),
#            'RF': RF(eqd),
#            },
#        'risk/return profile': {
#            'sharpe': sharpe(eqd),
#            'sortino': sortino(eqd),
#            'maxdd': maxdd(eqd),
#            'WCDD (monte-carlo {} quantile)'.format(quantile): mcmdd(eqd, quantile=quantile),
#            'UPI': UPI(eqd),
#            'MPI': MPI(eqd),
#            }
#        })
    
    return _format_out({
#        'backtest': {
#            'from': str(start(eqd)),
#            'to': str(end(eqd)),
#            'days': days(eqd),
#            'trades': len(eqd),
#            },
        'performance': {
            'p_y_r': profit_yy(eqd),
            'b_y_r': profit_yy(bl),
#            'averages': {
#                'trade': average(eqd),
#                'gain': average_gain(eqd),
#                'loss': average_loss(eqd),
#                },
            'winrate': winrate(eqd),
            'payoff': payoff(eqd),
#            'PF': PF(eqd),
#            'RF': RF(eqd),
            'alpha': alpha(eqd, bl),
            'beta': beta(eqd, bl)
            },
        'risk/return profile': {
            'maxdd': maxdd(eqd),
            'sharpe': sharpe(eqd),
            'sortino': sortino(eqd),
            'calmar': calmar(eqd)
#            'ir': ir(eqd, bl),
#            'WCDD (monte-carlo {} quantile)'.format(quantile): mcmdd(eqd, quantile=quantile),
#            'UPI': UPI(eqd),
#            'MPI': MPI(eqd)
            }
        })
    
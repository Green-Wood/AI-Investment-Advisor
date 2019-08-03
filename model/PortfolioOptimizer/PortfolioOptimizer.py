from math import sqrt
from cvxopt import matrix
from cvxopt.blas import dot
from cvxopt.solvers import qp
import cvxopt
import numpy as np


class PortfolioOptimizer:
    """
    PortfolioOptimizer

    Solve portfolio optimization problem.

    Parameters
    ----------
    expected_returns : Series
        Expected returns of assets, index is identifiers
        for different funds.

    cov_matrix : DataFrame
        Covariance matrix of funds. Index and columns are identifiers
        for different funds.

    """

    def __init__(self, expected_returns, cov_matrix, risk_free_rate=0.02):
        self.mu = expected_returns
        self.cov = cov_matrix
        self.num_assets = len(self.mu)
        self.risk_free_rate = risk_free_rate

    def optimize(self, N=100, show_progress=False):
        """
        Solve the problem with different parameters and store the answers. This method
        costs about 140 seconds when N = 100.

        Parameters
        ----------
        N : int
            Number of points to calculate, defaults to 100.

        show_progress : bool
            Whether to show optimization progress.

        Returns
        -------
        None

        """
        self.returns, self.risks, self.sharpe, self.weights = self.__optimize(self.cov.columns, self.mu, self.cov, N, show_progress)

    def get_fixed_ans(self, fixed='sharpe', value=0.05):
        """
        Get the closest answer with fixed parameter.
        NOTICE: Call optimize() before calling this method.

        Parameters
        ----------

        fixed : str, 'sharpe' or 'volatility' or 'return'
                Optimization constraints, defaults to 'sharpe'.

        value : float
                Optimization constraints. No need to set if fixed is
                'sharpe', defaults to 0.05.

        Returns
        -------
        answer : tuple, (float, float, float, dict)
                The closest answer given fixed constraints.
                (return, volatility, Sharpe ratio, weights)

        """

        if fixed == 'sharpe':
            idx = self.sharpe.index(max(self.sharpe))
        elif fixed == 'volatility':
            idx = self.risks.index(min(self.risks, key=lambda x: abs(x - value)))
        elif fixed == 'return':
            idx = self.returns.index(min(self.returns, key=lambda x: abs(x - value)))
        else:
            raise ValueError("fixed should be 'sharpe' or 'volatility' or 'return'"
                             " %s was provided." % str(fixed))
        return self.returns[idx], self.risks[idx], self.sharpe[idx], self.weights[idx]

    def get_all_ans(self):
        """
        Get all caculated answers.

        Returns
        -------
        answers : tuple, (list of float, list of float, list of float, list of dict)
            (list of returns, list of volatility, list of Sharpe ratio, list of weight)
        """
        return self.returns, self.weights, self.sharpe, self.weights

    def efficient_frontier(self, columns='all'):
        """
        Calculate efficient frontier of given funds.

        Parameters
        ----------
        columns : str or list of str, 'all' or ['id1', 'id2', ...]
                Funds to use to get efficient frontier. Use 'all' only
                if optimize() has been called. Otherwise use less than
                40 funds to make time cost acceptable.

        Returns
        -------
        performance : list of tuples, [(float, float, float),...,(float,float,float)]
                Each tuple is (expected return, volatility, Sharpe ratio).
        """
        if columns != 'all':
            t_mu = self.mu.loc[columns]
            t_cov = self.cov.loc[columns, columns]
            return self.__optimize(columns, t_mu, t_cov, N=50)
        else:
            return self.returns, self.risks, self.sharpe, self.weights

    def __optimize(self, names, mu, cov, N, show_progress=False):
        n = len(mu)
        S = matrix(cov.values)
        pbar = matrix(mu.values)
        G = matrix(0.0, (n, n))
        G[::n + 1] = -1.0
        h = matrix(0.0, (n, 1))
        A = matrix(1.0, (1, n))
        b = matrix(1.0)

        cvxopt.solvers.options['show_progress'] = show_progress
        mus = [10 ** (5 * t / N - 1.0) for t in range(N)]
        portfolios = [qp(float(t) * S, -pbar, G, h, A, b)['x'] for t in mus]
        returns = [dot(pbar, x) for x in portfolios]
        risks = [sqrt(dot(x, S * x)) for x in portfolios]
        sharpe = [(returns[i] - self.risk_free_rate) / (risks[i]+1e-4) for i in range(N)]
        weights = [dict(zip(names, portfolio)) for portfolio in portfolios]

        return returns, risks, sharpe, weights

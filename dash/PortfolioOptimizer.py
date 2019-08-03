from math import sqrt
from cvxopt import matrix
from cvxopt.blas import dot
from cvxopt.solvers import qp
import cvxopt


class PortfolioOptimizer:
    """
    PortfolioOptimizer

    Solves portfolio optimization problem.

    Parameters
    ----------
    data : DataFrame
        Full data without missing values, columns are identifiers
        for different funds, index is datetime.

    expected_returns : Series
        Expected returns of assets, index is identifiers
        for different funds.

    cov_matrix : DataFrame
        Covariance matrix of funds. Index and columns are identifiers
        for different funds.

    """

    def __init__(self, data, expected_returns, cov_matrix, risk_free_rate=0.02):
        self.data = data
        self.mu = expected_returns
        self.cov = cov_matrix
        self.num_assets = len(self.mu)
        self.risk_free_rate = risk_free_rate

    def optimize(self, N=100):
        """Solve the problem with different parameters and store the answers. This method
            costs about 140 seconds when N = 100.

            Parameters
            ----------
            N : int
                Number of points to calculate, defaults to 100.

            Returns
            -------
            self

        """
        self.returns, self.risks, self.sharpe, self.weights = self.__optimize(self.data.columns, self.mu, self.cov, N)

        return self

    def get_fixed_ans(self, fixed='sharpe', value=0.05):
        """Get the closest answer with fixed parameter.
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
            answer : tuple, (float, float, float)
                    The closest answer given fixed constraints.
                    (return, volatility, Sharpe ratio)

        """

        if fixed == 'sharpe':
            id = self.sharpe.index(max(self.sharpe))
        elif fixed == 'volatility':
            id = self.risks.index(min(self.risks, key=lambda x: abs(x - value)))
        elif fixed == 'return':
            id = self.returns.index(min(self.returns, key=lambda x: abs(x - value)))
        else:
            raise ValueError("fixed should be 'sharpe' or 'volatility' or 'return'"
                             " %s was provided." % str(fixed))
        return self.returns[id], self.risks[id], self.sharpe[id], self.weights[id]

    def get_all_ans(self):
        """Get all caculated answers.

            Returns
            -------
            answers : tuple, (list of float, list of float, list of float, list of dict)
                (list of returns, list of volatility, list of Sharpe ratio, list of weight)
        """
        return self.returns, self.risks, self.sharpe, self.weights

    def efficient_frontier(self, columns='all', risk_free_rate=0.02):
        """Calculate efficient frontier of given funds.
            Parameters
                ----------
                columns : str or list of str, 'all' or ['id1', 'id2', ...]
                        Funds to use to get efficient frontier. Use 'all' only
                        if optimize() has been called. Otherwise use less than
                        40 funds to make time cost acceptable.

                risk_free_rate : float
                    Risk free rate, defaults to 0.02.

                Returns
                -------
                performance : list of tuples, [(float, float, float),...,(float,float,float)]
                        Each tuple is (expected return, volatility, Sharpe ratio).
        """
        if columns != 'all':
            t_mu = self.mu.loc[columns]
            t_cov = self.cov.loc[columns, columns]
            return self.__optimize(columns, t_mu, t_cov, N=30)
        else:
            return self.returns, self.risks, self.sharpe, self.weights

    def __optimize(self, names, mu, cov, N):
        n = len(mu)
        S = matrix(cov.values)
        pbar = matrix(mu.values)
        G = matrix(0.0, (n, n))
        G[::n + 1] = -1.0
        h = matrix(0.0, (n, 1))
        A = matrix(1.0, (1, n))
        b = matrix(1.0)

        cvxopt.solvers.options['show_progress'] = False
        mus = [10 ** (5.0 * t / N - 1.0) for t in range(N)]
        portfolios = [qp(t * S, -pbar, G, h, A, b)['x'] for t in mus]
        returns = [dot(pbar, x) for x in portfolios]
        risks = [sqrt(dot(x, S * x)) for x in portfolios]
        sharpe = [(returns[i] - self.risk_free_rate) / risks[i] for i in range(N)]
        weights = []
        for portfolio in portfolios:
            w = {}
            for name, weight in zip(names, portfolio):
                w[name] = weight
            weights.append(w)
        return returns, risks, sharpe, weights

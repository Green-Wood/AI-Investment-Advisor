from math import sqrt
from cvxopt import matrix
from cvxopt.blas import dot
from cvxopt.solvers import qp
import cvxopt
import threading
import numpy as np
import heapq


class PortfolioOptimizer:
    """
    PortfolioOptimizer

    Solve portfolio optimization problem.

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

    def __init__(self, expected_returns, cov_matrix, risk_free_rate=0.02):
        self.mu = expected_returns
        self.cov = cov_matrix
        self.num_assets = len(self.mu)
        self.risk_free_rate = risk_free_rate

    def optimize(self, N=100, n_threads=4, show_progress=False):
        """
        Solve the problem with different parameters and store the answers. This method
        costs about 140 seconds when N = 100.

        Parameters
        ----------
        N : int
            Number of points to calculate, defaults to 100.

        n_threads : int
            Number of threads. Notice that too many threads may decrease efficiency.

        show_progress : bool
            Whether to show optimization progress.

        Returns
        -------
        None

        """
        self.returns, self.risks, self.sharpe, self.weights = self.__optimize(self.cov.columns, self.mu, self.cov, N, show_progress, n_threads)

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

    def get_random_samples(self,weights,num_funds=7,num_portfolios=1000):
        """Return random portfolios.

        :param weights: dict
            Weights of a portfolio. Weights corresponding to fixed risk = 0.05
            is recommended.
        :param num_funds: int
            Number of funds used to sample random portfolios.
        :param num_portfolios: int
            Number of portfolios to sample.
        :return: list,list,list
            returns, risks, Sharpe ratio
        """
        n_large=heapq.nlargest(num_funds,weights.values())[-1]
        columns=[k for k,v in weights.items() if v>=n_large]
        t_mu = self.mu.loc[columns]
        t_cov = self.cov.loc[columns, columns]
        n=len(columns)
        results = np.zeros((3, num_portfolios))
        for i in range(num_portfolios):
            weights = np.random.random(n)
            weights /= np.sum(weights)
            portfolio_std_dev=sqrt(np.dot(weights.T,np.dot(t_cov,weights)))
            portfolio_return = np.dot(weights.T, t_mu)
            results[0, i] = portfolio_std_dev
            results[1, i] = portfolio_return
            results[2, i] = (portfolio_return - self.risk_free_rate) / portfolio_std_dev
        return list(results[1,:]),list(results[0,:]),list(results[2,:])

    def __optimize(self, names, mu, cov, N, show_progress=False, n_threads=4):
        n = len(mu)
        S = matrix(cov.values)
        pbar = matrix(mu.values)

        # G = matrix(0.0, (2*n, n))
        # G[::(2*n+1)] = -1.0
        # G[n::(2*n+1)] = 1.0
        # h = matrix(0.0, (2*n, 1))
        # h[n:] = 0.1

        G = matrix(0.0, (n, n))
        G[::n + 1] = -1.0
        h = matrix(0.0, (n, 1))

        A = matrix(1.0, (1, n))
        b = matrix(1.0)

        threads=[]
        mus = [10 ** (5 * t / N - 1.0) for t in range(N)]
        chunks=[mus[i:int(i+N/n_threads)] for i in range(0,len(mus),int(N/n_threads))]
        if len(chunks)==N+1:
            chunks[-2].extend(chunks[-1])
            chunks.pop()

        for i in range(n_threads):
            threads.append(OptimizeThread(i,chunks[i],S,pbar,G,h,A,b,names,
                                          self.risk_free_rate,show_progress))
            threads[-1].start()

        for t in threads:
            t.join()

        returns,risks,sharpe,weights=[],[],[],[]

        for t in threads:
            treturns, trisks, tsharpe, tweights=t.get_ans()
            returns.extend(treturns)
            risks.extend(trisks)
            sharpe.extend(tsharpe)
            weights.extend(tweights)

        return returns, risks, sharpe, weights


class OptimizeThread(threading.Thread):
    def __init__(self,thread_id,mus,S,pbar,G,h,A,b,names,risk_free_rate=0.02,show_progress=False):
        threading.Thread.__init__(self)
        self.thread_id=thread_id
        self.mus=mus
        self.S=S
        self.pbar=pbar
        self.G=G
        self.h=h
        self.A=A
        self.b=b
        self.risk_free_rate=risk_free_rate
        self.show_progress=show_progress
        self.names=names

    def run(self):
        cvxopt.solvers.options['show_progress'] = self.show_progress
        self.portfolios = [qp(float(t) * self.S, -self.pbar, self.G, self.h, self.A, self.b)['x'] for t in self.mus]
        self.returns = [dot(self.pbar, x) for x in self.portfolios]
        self.risks = [sqrt(dot(x, self.S * x)) for x in self.portfolios]
        self.sharpe = [(self.returns[i] - self.risk_free_rate) / (self.risks[i] + 1e-4) for i in range(len(self.returns))]
        self.weights = [dict(zip(self.names, portfolio)) for portfolio in self.portfolios]

    def get_ans(self):
        return self.returns, self.risks, self.sharpe, self.weights

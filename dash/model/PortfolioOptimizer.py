from pypfopt.efficient_frontier import EfficientFrontier
import pypfopt.expected_returns as expected_returns
import pypfopt.risk_models as risk_models
import pandas as pd
import numpy as np
from functools import reduce
import scipy.optimize as sco
import pypfopt.objective_functions as funcs


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

    def __init__(self,data,expected_returns,cov_matrix):
        self.data=data
        self.mu=expected_returns
        self.cov=cov_matrix
        self.num_assets=len(self.mu)
        self.ef=EfficientFrontier(self.mu,self.cov)

    def optimize(self,method='cluster',fixed='sharpe',
                 value=0.05,risk_free_rate=0.02):
        """Get the optimized weights.

            Parameters
            ----------
            method : str, 'cluster' or 'direct'
                    Method to solve the problem. Use 'cluster' when
                    number of funds is large, like 200. Use 'direct'
                    o.w. Defaults to 'cluster'.

            fixed : str, 'sharpe' or 'volatility' or 'return'
                    Optimization constraints, defaults to 'sharpe'.

            value : float
                    Optimization constraints. No need to set if fixed is
                    'sharpe', defaults to 0.05.

            risk_free_rate : float
                    Risk free rate, defaults to 0.02.

            Returns
            -------
            weights : dict
                    Weight for different fund. Key is fund identifier,
                    value is weight.

        """
        if method=='cluster':
            t_mu,t_cov,weight_list=self.__get_clustered_statistics()
        elif method=='direct':
            t_mu, t_cov=self.mu,self.cov
        else:
            raise ValueError("method should be 'cluster' or 'direct'."
                             " %s was provided." % str(method))
        ef = EfficientFrontier(t_mu, t_cov)
        if fixed == 'sharpe':
            cluster_weight=ef.max_sharpe(risk_free_rate)
        elif fixed == 'volatility':
            cluster_weight=self.__fixed_risk(t_mu,t_cov,value)
        elif fixed == 'return':
            cluster_weight=ef.efficient_return(value)
        else:
            raise ValueError("fixed should be 'sharpe' or 'volatility' or 'return'"
                             " %s was provided." % str(fixed))
        if method=='direct':
            self.ef.weights=cluster_weight
        else:
            total_weights = {}
            for cluster_id, weights in enumerate(weight_list):
                for asset_id, w in weights.items():
                    total_weights[asset_id] = cluster_weight[cluster_id] * w
            new_names=[]
            for k,v in total_weights.items():
                if v>1e-8:
                    new_names.append(k)
            if len(new_names)>150:
                new_names=new_names[:150]
            print("size= "+str(len(new_names)))
            new_mu=self.mu.loc[new_names]
            new_cov=self.cov.loc[new_names,new_names]
            ef=EfficientFrontier(new_mu,new_cov)
            if fixed == 'sharpe':
                weights = ef.max_sharpe(risk_free_rate)
            elif fixed == 'volatility':
                weights = self.__fixed_risk(new_mu,new_cov,value)
            elif fixed == 'return':
                weights = ef.efficient_return(value)
            for name in self.data.columns:
                if name not in new_names:
                    weights[name]=0
            self.ef.weights=weights
        return self.ef.weights

    def performance(self,verbose=False):
        """After optimising, calculate (and optionally print) the performance
        of the optimal portfolio.

            Parameters
            ----------
            verbose : bool
                    Whether performance should be printed, defaults to False.

            Returns
            -------
            performance : tuple, (float, float, float)
                    Expected return, volatility, and the Sharpe ratio.

        """
        print(type(self.ef.weights))
        return self.ef.portfolio_performance(verbose)

    def efficient_frontier(self,columns='all',risk_free_rate=0.02):
        """Calculate efficient frontier of given funds.
            Parameters
                ----------
                columns : str or list of str, 'all' or ['id1', 'id2', ...]
                        Funds to use to get efficient frontier. 'all' means
                        all funds will be used, which is not suggested. Just
                        use less than 40 funds to make time cost acceptable.

                risk_free_rate : float
                    Risk free rate, defaults to 0.02.

                Returns
                -------
                performance : list of tuples, [(float, float, float),...,(float,float,float)]
                        Each tuple is (expected return, volatility, Sharpe ratio).
        """
        if columns != 'all':
            t_mu=self.mu.loc[columns]
            t_cov=self.cov.loc[columns,columns]
        else:
            t_mu=self.mu
            t_cov=self.cov
        results=[]
        ef=EfficientFrontier(t_mu,t_cov)

        ef.min_volatility()
        r1,v_begin,sharpe1=ef.portfolio_performance()

        ef.weights=self.__fixed_risk(t_mu, t_cov, 0.5)
        r3,v_end,sharpe3=ef.portfolio_performance()

        target=np.linspace(v_begin,v_end,6,endpoint=False)

        for x in target:
            ef.weights=self.__fixed_risk(t_mu, t_cov, x)
            results.append(ef.portfolio_performance(True,risk_free_rate=risk_free_rate))

        results.append((r3, v_end, sharpe3))
        return results

    def __get_clustered_statistics(self):
        num_clusters=int(self.num_assets/100)+1
        names=self.data.columns
        labels = [int(i / 100) for i in range(self.num_assets)]

        cluster_data_lists = [[] for i in range(num_clusters)]

        for i, label in enumerate(labels):
            cluster_data_lists[label].append(names[i])

        for i, data_name_list in enumerate(cluster_data_lists):
            cluster_data_lists[i] = self.data[data_name_list]

        new_mu = pd.Series(data=np.zeros(num_clusters))

        weight_list = []

        for i, subdata in enumerate(cluster_data_lists):
            if subdata.shape[1] == 1:
                weight_list.append({subdata.columns[0]: 1.0})
            else:
                t_mu = expected_returns.ema_historical_return(subdata)
                t_cov = risk_models.CovarianceShrinkage(subdata).ledoit_wolf()
                t_ef = EfficientFrontier(t_mu, t_cov)
                t_ans = t_ef.max_sharpe()
                weight_list.append(t_ans)

        for i in range(num_clusters):
            new_mu[i] = reduce(lambda x, y: x + y, [value * self.mu.loc[key]
                                                    for key, value in weight_list[i].items()])

        new_data = pd.concat([reduce(lambda x, y: x + y,
                                     [cluster_data_lists[i][asset_name].fillna(
                                         cluster_data_lists[i][asset_name].mean()) * w
                                      for asset_name, w in weight_list[i].items()])
                              for i in range(len(cluster_data_lists))], axis=1)

        new_cov = risk_models.CovarianceShrinkage(new_data).ledoit_wolf()
        return new_mu,new_cov,weight_list

    def __fixed_risk(self, mu, cov, target_risk):
        num_assets=len(mu)
        args = (mu)

        def vol(x):
            return funcs.volatility(x,cov)

        constraints = ({'type': 'eq', 'fun': lambda w: target_risk - np.sqrt(funcs.volatility(w, cov))})

        bounds = tuple((0, 1) for asset in range(num_assets))

        result = sco.minimize(funcs.negative_mean_return, num_assets * [1. / num_assets, ], args=args,
                              method='SLSQP',
                              bounds=bounds,
                              constraints=constraints)
        weights = result["x"]
        return dict(zip(cov.columns, weights))


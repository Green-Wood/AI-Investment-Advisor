from pypfopt.efficient_frontier import EfficientFrontier
import pypfopt.expected_returns as expected_returns
import pypfopt.risk_models as risk_models
import pandas as pd
import os
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from sklearn.covariance import ShrunkCovariance
from time import time
from functools import reduce

if __name__ == '__main__':
    start = time()
    min_num_not_nan = 30

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", action='store', type=str, default=".")
    parser.add_argument("-s", "--subdirs", action='store', type=str, default="all")
    parser.add_argument("-v", "--volatility", action='store', type=float, default=-1)
    parser.add_argument("-r", "--risk_free_rate", action='store', type=float, default=0.02)
    parser.add_argument("-c", "--num_cluster", action='store', type=int, default=200)
    args = parser.parse_args()

    nav_path = args.path
    # "C:/Users/qin_t/Desktop/PortfolioOptimization/funds/funds/nav"
    dateparser = lambda x: pd.datetime.strptime(x, "%Y-%m-%d")
    data_lists = []
    names = []
    for subdir in (os.listdir(nav_path) if args.subdirs == "all" else args.subdirs.split(',')):
        print(subdir)
        data_lists.append([])
        if not os.path.isdir(nav_path + "/" + subdir):
            continue
        for filename in os.listdir(nav_path + "/" + subdir):
            filepath = nav_path + "/" + subdir + "/" + filename

            tdata = pd.read_csv(str(filepath),
                                parse_dates=['datetime'],
                                index_col='datetime',
                                date_parser=dateparser  # 按时间对齐
                                )
            if tdata.shape[0] < 100:  # 忽略小于100行的文件
                continue
            if 'adjusted_net_value' in tdata.columns and not np.isnan(tdata['adjusted_net_value']).all():  # 非日结
                if tdata['adjusted_net_value'].max() > 10:  # 忽略有数据大于10的文件
                    continue
                data_lists[-1].append(
                    tdata[['adjusted_net_value']]
                        .rename(columns={'adjusted_net_value': filename[0:6]}, index=str).astype('float'))
            elif 'daily_profit' in tdata.columns and not np.isnan(tdata['daily_profit']).all():  # 日结
                data_lists[-1].append(
                    (tdata[['daily_profit']] / 10000 + 1).cumprod(axis=1)
                        .rename(columns={'daily_profit': filename[0:6]}, index=str).astype('float'))
            else:
                print("BAD file: " + filename)
        data_lists[-1] = pd.concat(data_lists[-1], axis=1)

    data = pd.concat(data_lists, axis=1).dropna(axis=1, thresh=min_num_not_nan)

    print(data.info())
    names = data.columns

    cov = risk_models.CovarianceShrinkage(data).ledoit_wolf()
    var = np.eye(cov.shape[0]) * cov
    std = np.power(var, 0.5)
    I = np.linalg.inv(std)
    corr = I.dot(cov).dot(I)
    corr_dist_matrix = 1 - corr

    clustering = AgglomerativeClustering(n_clusters=args.num_cluster,
                                         affinity="precomputed",
                                         memory="C:/Users/qin_t/Desktop/PortfolioOptimization/notebook",
                                         linkage="average").fit(corr_dist_matrix)

    # selected = {}
    # selected_count = {}
    # for i, label in enumerate(clustering.labels_):
    #     if not label in selected:
    #         selected[label] = i
    #         selected_count[label] = 1
    #     else:
    #         selected_count[label] += 1
    #         if np.random.uniform() < 1.0 / selected_count[label]:
    #             selected[label] = i
    # selected_names = [names[x] for x in selected.values()]
    #
    # selected_data = data[selected_names].dropna(axis=1, how='all', thresh=2)
    # mu = expected_returns.ema_historical_return(selected_data)
    # S = risk_models.CovarianceShrinkage(selected_data).ledoit_wolf()
    # ef = EfficientFrontier(mu, S)
    #
    # if args.volatility < 0:
    #     print(ef.max_sharpe(args.risk_free_rate))
    # else:
    #     print(ef.efficient_risk(args.volatility, args.risk_free_rate))
    #
    # ef.portfolio_performance(True)
    #
    # print(str(time() - start) + " s")

    mu = expected_returns.ema_historical_return(data)

    cluster_data_lists = [[] for i in range(args.num_cluster)]

    for i, label in enumerate(clustering.labels_):
        cluster_data_lists[label].append(names[i])

    for i, data_name_list in enumerate(cluster_data_lists):
        cluster_data_lists[i] = data[data_name_list]

    print(len(cluster_data_lists))

    new_mu = pd.Series(data=np.zeros(args.num_cluster))
    new_cov = pd.DataFrame(data=np.zeros((args.num_cluster, args.num_cluster)))
    print(new_cov.head())

    weight_list = []

    for i, subdata in enumerate(cluster_data_lists):
        # print(str(i)+" "+str(subdata.shape[1]))
        if subdata.shape[1] == 1:
            weight_list.append({subdata.columns[0]: 1.0})
        else:
            if subdata.shape[1] > 50:  # 同一簇中数量过多时随机选择50支基金
                subdata = subdata.iloc[:, np.random.choice(subdata.shape[1], 50)]
            t_mu = expected_returns.ema_historical_return(subdata)
            t_cov = risk_models.CovarianceShrinkage(subdata).ledoit_wolf()
            t_ef = EfficientFrontier(t_mu, t_cov)
            t_ans = t_ef.max_sharpe()
            for asset in cluster_data_lists[i].columns:
                if asset not in t_ans:
                    t_ans[asset] = 0.0
            weight_list.append(t_ans)

    for i in range(args.num_cluster):
        new_mu[i] = reduce(lambda x, y: x + y, [value * mu.loc[key] for key, value in weight_list[i].items()])

    new_data = pd.concat([reduce(lambda x, y: x + y,
                                 [cluster_data_lists[i][asset_name].fillna(cluster_data_lists[i][asset_name].mean()) * w
                                  for asset_name, w in weight_list[i].items()])
                          for i in range(len(cluster_data_lists))], axis=1)

    new_cov = risk_models.CovarianceShrinkage(new_data).ledoit_wolf()

    # print(new_mu)

    # print(new_cov)

    total_ef = EfficientFrontier(new_mu, new_cov)

    if args.volatility < 0:
        cluster_weight = total_ef.max_sharpe(args.risk_free_rate)
    else:
        cluster_weight = total_ef.efficient_risk(args.volatility, args.risk_free_rate)

    total_weight = {}
    for cluster_id, weights in enumerate(weight_list):
        for asset_id, w in weights.items():
            total_weight[asset_id] = cluster_weight[cluster_id] * w

    print(len(total_weight))

    final_ef = EfficientFrontier(mu, cov)
    final_ef.weights = total_weight
    print(total_weight)
    final_ef.portfolio_performance(True)

    print(str(time() - start) + " s")

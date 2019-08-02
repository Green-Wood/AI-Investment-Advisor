
# 命令行参数
- -p nav文件路径，如 -p C:/Users/xxx/funds/nav
- -key 需要提取的数据，如单位净值数据 adjusted_net_value ,可选字段unit_net_value	acc_net_value	adjusted_net_value	subscribe_status
  redeem_status  (日收益、7日年化数据符合要求的仅100多支基金，建议舍弃)
- -u 输出的csv文件的位置，输出结构为时间\*基金号(1227\*1258)，数值为key的值


# 示例
```
python data_cleaning.py -p /Users/wesley/Portfolio/data/funds/nav -key adjusted_net_value -out /Users/wesley/Portfolio/data/funds
```
输出：
```
49
40
47
78
13
14
22
25
  data = pd.concat(data_list, axis=1)
            519661  000061  398061  519995  ...  161625  270025  180025  110025
2014-01-02   1.008   0.747   1.163  0.5504  ...   0.924   1.019   1.045   0.644
2014-01-03   1.006   0.747   1.172  0.5460  ...   0.921   1.021   1.045   0.637
2014-01-06   1.006   0.735   1.149  0.5350  ...   0.914   0.990   1.045   0.621
2014-01-07   1.006   0.741   1.167  0.5354  ...   0.914   1.005   1.045   0.619
2014-01-08   1.006   0.746   1.179  0.5342  ...   0.913   1.017   1.048   0.613

[5 rows x 1258 columns]
```

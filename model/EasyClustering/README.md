# 算法说明
- 忽略数据少于100条，或者存在明显数据异常（>10）的文件
- 计算全部基金收益的相关系数矩阵corr，将 1-corr 作为距离矩阵进行聚类（类数目 c 可通过命令行参数指定）
- 在第i个簇内使用Markowitz模型求解最大化Sharpe Ratio的权重向量wi（为加速运算，当簇内基金数大于50时随机选取50支进行计算）
- 将第i簇的基金按wi加权，得到第i簇的“代表元”vi
- 对c个“代表元”使用Markowitz模型求解，得到权重向量w'，则第i个簇内的基金权重为w'_i * wi
# 使用说明
```
pip install PyPortfolioOpt
```

# 命令行参数
- -p nav文件路径，如 -p C:/Users/xxx/funds/nav
- -s 使用的子文件夹名，如使用nav/00和nav/01下的数据，则 -s 00,01，默认使用全部文件夹下的数据
- -v 可接受的年化风险，若使用默认值则输出最大sharpe ratio对应的解，否则输出对应风险下最大收益对应的解
- -r 为risk free rate，默认0.02
- -c 为聚类所得簇的数量，默认200

# 示例
```
python -p C:\Users\xxx\funds\nav
```
输出：
```
{'000200': 0.02704022476877448, ..., '960000': 0.0}
Expected annual return: 22.9%
Annual volatility: 7.1%
Sharpe Ratio: 2.94
246.2807 s
```
3-7分钟可完成。


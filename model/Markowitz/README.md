# 使用说明
- pip install PyportfolioOpt
- [用户手册](https://pyportfolioopt.readthedocs.io/en/latest/index.html)

# 命令行参数
- -p nav文件路径，如 -p C:/Users/xxx/funds/nav
- -s 使用的子文件夹名，如使用nav/00和nav/01下的数据，则 -s 00,01，默认使用全部文件夹下的数据
- -v 可接受的年化风险，若使用默认值则输出最大sharpe rate对应的解，否则输出对应风险下最大收益对应的解
- -r 为risk free rate，默认0.02

# 示例
```
python -p C:\Users\xxx\funds\nav -s 00 -v 0.04
```
输出：
```
{'000200': 0.02704022476877448, ..., '960000': 0.0}
Expected annual return: 10.8%
Annual volatility: 4.0%
Sharpe Ratio: 2.19
```


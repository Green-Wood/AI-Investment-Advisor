# 使用说明
- pip install fbprophet
- Facebook出的时间序列预测工具fbprophet，有不少功能暂时没有放在这个程序里,有些参数因为太多的缘故没有设置外部可调。另外只做了单基金的，大家熟悉了之后可以随便改。
- [用户手册](https://facebook.github.io/prophet/docs/quick_start.html#python-api)
- [参考博客](https://blog.csdn.net/anshuai_aw1/article/details/83412058)

# 命令行参数
- -p nav文件路径，如 -p C:/Users/xxx/funds/nav
- -s 使用的子文件夹名，如 -s 01 默认 00
- -f 基金ID，如 -f 000400 默认 000300
- -t 训练集大小，如 -t 0.7 默认 0.9
- -pe 预测天数，如 -pe 100 默认 300
- -c 趋势灵活性,即拟合程度，越大拟合程度越高，如 -c 0.5 默认 0.05
- -an 是否分析模型，如 -an False 默认True

# 示例
```
python fbprophet_predict.py -p C:\Users\xxx\funds\nav -s 00 -f 000400 -t 0.7 -pe 100 -c 0.5 -an True
```

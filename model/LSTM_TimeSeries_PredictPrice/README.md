### 1、算法功能

1、用LSTM网络实现单只基金的未来30天的价格预测

2、用预测的价格使用[Efficient Frontier Portfolio Optimisation in Python]([https://towardsdatascience.com/efficient-frontier-portfolio-optimisation-in-python-e7844051e7f?gi=e8ff76cda240](https://towardsdatascience.com/efficient-frontier-portfolio-optimisation-in-python-e7844051e7f?gi=e8ff76cda240))方法实现基金权重的配比

### 2、使用方法

1、根据第一个cell代码安装所需要的包，以及tensoflow

2、按照步骤顺序执行代码

3、运行时需要更改文件的加载路径

4、LSTM网络的超参数可以根据自己需求调整

### 3、其他说明

1、算法LSTM的执行时间：时间主要花在神经网络的构建上，经测试，平均一支基金运行时间在5秒左右，总共4000+基金总共使用4+小时

2、服务器配置：32G内存 未使用GPU

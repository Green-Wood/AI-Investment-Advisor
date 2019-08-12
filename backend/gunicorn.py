import multiprocessing

bind = '0.0.0.0:5000'  # 绑定ip和端口号

worker_class = 'gevent'  # 使用gevent模式，还可以使用sync 模式，默认的是sync模式

workers = multiprocessing.cpu_count() * 2 + 1  # 进程数

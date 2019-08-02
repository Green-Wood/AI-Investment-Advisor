from time import time
import pandas as pd
import os
import argparse
import numpy as np


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--path", action='store',type=str,default=".")
    parser.add_argument("-key","--key_value", action='store',type=str,default=".")
    parser.add_argument("-out","--output_dirs",action='store',type=str,default=".")


    args=parser.parse_args()

    nav_path = args.path
    key = args.key_value
    # dateparser = lambda x: pd.datetime.strptime(x, "%Y-%m-%d")
    data_list = []
    out_path = args.output_dirs

    for subdir in os.listdir(nav_path):
        print(subdir)
        if not os.path.isdir(nav_path + "/" + subdir):
            continue
        for filename in os.listdir(nav_path + "/" + subdir):
            filepath = nav_path + "/" + subdir + "/" + filename
            tdata = pd.read_csv(str(filepath),index_col='datetime')
            if filename == '511880.csv':  #网络图异常数据点
                continue
            if len(tdata) != 1226 and len(tdata) != 1483:
                continue
            if key in tdata.columns and not np.isnan(tdata[key]).all(): # 非日结
                data_list.append(
                    tdata[[key]].rename(columns={key: filename[0:6]}, index=str).astype('float'))
            else:
                # print("BAD file: "+filename)
                continue
    data = pd.concat(data_list, axis=1) #对齐移位
    data.iloc[154,731]  = data.iloc[153,731]
    da = data.drop('2014-08-17',axis=0,inplace=False)
    print(da.head())
    da.to_csv(out_path + key + '.csv')






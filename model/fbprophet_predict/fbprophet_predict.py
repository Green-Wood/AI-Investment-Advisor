import numpy as np
import pandas as pd
from fbprophet import Prophet
from fbprophet.diagnostics import cross_validation,performance_metrics
from fbprophet.plot import plot_cross_validation_metric
import os
import datetime
import argparse



def Preprocessing_Data(nav_path,sub_folder, fund_id):

    filepath = nav_path + "/" + sub_folder + "/" + fund_id + '.csv'
    tdata = pd.read_csv(str(filepath))
    if 'unit_net_value' in tdata.columns:
        data = tdata.loc[:,['datetime','unit_net_value']].dropna(axis=1, how='any')
    else:
        data = tdata.loc[:, ['datetime', 'weekly_yield']].dropna(axis=1, how='any')

    train_x = data.iloc[:, 0]
    train_y = data.iloc[:, 1]

    return train_x,train_y


def Holiday_Data(start_date,end_date):

    start = datetime.datetime.strptime(start_date,'%Y/%m/%d')
    end = datetime.datetime.strptime(end_date,'%Y/%m/%d')
    days_off = [5, 6]
    tag_date = start
    weekend =[]
    while True:
        if tag_date > end:
            break
        if tag_date.weekday() in days_off:
            str_date = tag_date.strftime("%Y-%m-%d")
            weekend.append(str_date)
        tag_date += datetime.timedelta(days=1)

    return weekend



def FB_Model(train_x, train_y,train_ratio,predict_period,changepoint_prior_scale,analysisornot,holiday):
    time_split = int((train_x.shape[0]) * train_ratio)
    df = pd.DataFrame(columns=['ds', 'y'])
    df['ds'] = train_x[:time_split];df['y'] = train_y[:time_split]
    df['y'] = np.log((np.asarray(df['y'], dtype=float))) #log能让预测效果更好

    Hoday = pd.DataFrame({
        'holiday': 'weekend',
        'ds': pd.to_datetime(holiday),
        'lower_window': 0,
        'upper_window': 1,
    })

    #训练
    model = Prophet(changepoint_prior_scale=changepoint_prior_scale,mcmc_samples=0,holidays=Hoday)#默认为0，增大后将最大后验估计取代为马尔科夫蒙特卡洛取样，但是会极大地延长训练时间
    model.fit(df)
    future = model.make_future_dataframe(freq='D', periods=predict_period)  # 建立数据预测框架，数据粒度为天，预测步长为20天
    forecast = model.predict(future)
    model.plot(forecast).show()  # 绘制预测效果图
    model.plot_components(forecast).show()

    #分析结果
    if analysisornot:
        df_cv = cross_validation(model, initial='1100 days', period='20 days', horizon='20 days')
        df_p = performance_metrics(df_cv)
        print(df_cv.head())
        print(df_p.head())
        fig = plot_cross_validation_metric(df_cv, metric='mape')
        fig.show()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", action='store', type=str, default="D://python/MPT/data/funds/nav/")
    parser.add_argument("-s", "--sub_folder", action='store', type=str, default="00")
    parser.add_argument("-f", "--fund_id", action='store', type=str, default="000300")
    parser.add_argument("-t", "--train_ratio", action='store', type=float, default=0.9)
    parser.add_argument("-pe", "--predict_period", action='store', type=int, default=20)
    parser.add_argument("-c", "--changepoint_prior_scale", action='store', type=float, default=0.5)#趋势灵活性，越大拟合越强
    parser.add_argument("-an", "--analysis", action='store', type=bool, default=True)
    args = parser.parse_args()




    train_x, train_y= Preprocessing_Data(nav_path=args.path,
                                         sub_folder =args.sub_folder,
                                         fund_id=args.fund_id)

    weekends = Holiday_Data('2014/1/1', '2019/12/31')

    start_time = datetime.datetime.now()

    FB_Model(train_x, train_y,predict_period=args.predict_period,
             changepoint_prior_scale=args.changepoint_prior_scale,
             train_ratio=args.train_ratio,analysisornot=args.analysis,holiday=weekends)

    end_time = datetime.datetime.now()
    print("train time:",end_time-start_time)



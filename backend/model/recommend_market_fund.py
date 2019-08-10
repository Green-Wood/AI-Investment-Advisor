# coding: utf-8
import pandas as pd
import pathlib

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()


def get_recom_marker_fund(fund_weight):
    """
    :param fund_weight:
    dict
    {'161603': 0.3879186308239624, '161693': 9.121650701464391e-07, '161618': 2.090769995577721e-06}

    :return:
    three dict

    market_dict
    {'320021':
        {'fund_symbol': '诺安双利债券发起',
        'fund_type': '债券型',
        'fund_return': '40.54%',
        'other_ave': '8.00%',
        'weight': 0.3879190162512064},
    '161603':
        {'fund_symbol': '融通债券A/B',
        'fund_type': '债券型',
        'fund_return': '43.83%',
        'other_ave': '45.71%',
        'weight': 0.3879190162512064}}

    recom_dict
    {'000191':
        {'fund_symbol': '富国信用债债券A/B',
        'fund_type': '债券型',
        'fund_return': '33.19%',
        'other_ave': '38.52%'},
    '161618':
        {'fund_symbol': '融通岁岁添利定开债A',
        'fund_type': '定开债券',
        'fund_return': '30.18%',
        'other_ave': '22.98%'}}

    ratio_dict
        {'中低风险': 9,
        '中风险': 1,
        '未知': 1}
    """
    fund_weight_df = pd.DataFrame.from_dict(fund_weight, orient='index', columns=['values'])
    fund_weight_df = fund_weight_df[fund_weight_df['values'] > 1e-07]
    fund_weight_df = fund_weight_df.sort_values(by="values", ascending=False)
    market_fund_list = [int(i) for i in list(fund_weight_df.index)]

    corr_df = pd.read_csv(DATA_PATH.joinpath('corr.csv'), index_col=0)
    corr_df.drop(market_fund_list, inplace=True)
    recom_fund_list = list(
        corr_df[[str(market_fund_list[0]).zfill(6)]].sort_values(by=[str(market_fund_list[0]).zfill(6)],
                                                                 ascending=False).index)

    market_dict = {}
    recom_dict = {}
    show_df = pd.read_csv(DATA_PATH.joinpath('new_fund_type_manager.csv'), index_col=2, encoding='gb18030')

    for i in market_fund_list:
        market_dict[str(i).zfill(6)] = {
            'fund_symbol': show_df.loc[i]['基金名称'],
            'fund_type': show_df.loc[i]['基金类型'],
            'fund_return': show_df.loc[i]['任职回报'],
            'other_ave': show_df.loc[i]['同类平均'],
            'fund_risk': show_df.loc[i]['风险'],
            'weight': fund_weight[str(i).zfill(6)] / sum(fund_weight.values())
        }

    for i in recom_fund_list:
        recom_dict[str(i).zfill(6)] = {
            'fund_symbol': show_df.loc[i]['基金名称'],
            'fund_type': show_df.loc[i]['基金类型'],
            'fund_return': show_df.loc[i]['任职回报'],
            'other_ave': show_df.loc[i]['同类平均'],
            'fund_risk': show_df.loc[i]['风险']
        }

    raw_dict = {
        '高风险': 0,
        '中高风险': 0,
        '中低风险': 0,
        '低风险': 0,
        '中风险': 0,
        '未知': 0
    }

    ratio_dict = dict(show_df.loc[market_fund_list].groupby('风险')['风险'].count())

    ratio_dict = dict(raw_dict, **ratio_dict)
    ratio_dict = {k: int(v) for k, v in ratio_dict.items()}
    return market_dict, recom_dict, ratio_dict


if __name__ == "__main__":
    fund_weight = {'161603': 0.3879186308239624, '161693': 9.121650701464391e-07, '161618': 2.090769995577721e-06,
                   '160129': 1.0795319988134981e-07, '000187': 8.293637921281513e-07, '160128': 7.112348395991103e-07,
                   '161619': 1.7773816160230917e-07, '320021': 0.5641932299495023, '000186': 4.4709598109976884e-07,
                   '000191': 0.047881711242125924, '650001': 1.5808680347575287e-07}
    market_dict, recom_dict, ratio_dict = get_recom_marker_fund(fund_weight)
    print(market_dict)
    print('----------------------------------------------------')
    print(recom_dict)
    print('----------------------------------------------------')
    print(ratio_dict)

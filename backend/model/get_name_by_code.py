import pandas as pd
import pathlib

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()
path_adjusted_net_value = DATA_PATH.joinpath('adjusted_net_value.csv')
path_instruments = DATA_PATH.joinpath('instruments.csv')

instruments = pd.read_csv(path_instruments)


def get_name(code):
    """
    通过int代码，找到该基金的名字
    :param code:
    :return:
    """
    return instruments[instruments['code'] == code].iloc[0, 1]


if __name__ == '__main__':
    print(get_name(1))
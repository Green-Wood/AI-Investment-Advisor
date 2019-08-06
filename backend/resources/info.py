from flask_restplus import Resource, Namespace, reqparse, fields
from init_optmizer import optimizer
import pathlib
import pandas as pd

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("funds").resolve()
instruments = DATA_PATH.joinpath('instruments.csv')

api = Namespace('info', description='小程序分配页的信息')

_info_parser = reqparse.RequestParser()
_info_parser.add_argument('risk_value',
                          required=True,
                          type=int,
                          help='风险承受能力',
                          choices=(1, 2, 3, 4, 5))


ration_model = api.model(
    'ratio_model',
    {
        'Bond': fields.Float(default=0),
        'Hybrid': fields.Float(default=0),
        'QDII': fields.Float(default=0),
        'Stock': fields.Float(default=0),
        'Other': fields.Float(default=0),
        'Money': fields.Float(default=0),
        'Related': fields.Float(default=0),
    }
)

ans_model = api.model(
    'ans_model',
    {
        'Return': fields.Float,
        'Volatility': fields.Float,
        'SharpRatio': fields.Float
    }
)

info_model = api.model(
    'info_model',
    {
        'ans': fields.Nested(ans_model),
        'ratio': fields.Nested(ration_model)
    }
)


@api.route('')
class Allocator(Resource):

    @api.response(200, 'get info successfully', model=info_model)
    @api.expect(_info_parser)
    @api.marshal_list_with(info_model, envelope='info')
    def get(self):
        """
        根据用户风险获取基金分配的信息
        :param code:
        :return:
        """
        args = _info_parser.parse_args()
        risk_val = args['risk_value'] / 100
        ret, vol, sharp, weight = optimizer.get_fixed_ans('volatility', risk_val)

        try:
            data = pd.read_csv(instruments)
        except:
            print('Error!:instruments.csv的路径错误，请核对')
            return ''
        data_dic = {
            'Hybrid': 0,
            'Bond': 0,
            'Stock': 0,
            'QDII': 0,
            'Money': 0,
            'Related': 0,
            'Other': 0
        }
        for key in weight.keys():
            idx = list(data['code']).index(int(key))
            a_type = data['fund_type'][idx]
            data_dic[a_type] = data_dic[a_type] + weight[key]
        # sum = 0
        # for key in data_dic.keys():
        #     sum = sum + data_dic[key]
        # for key in data_dic.keys():
        #     data_dic[key] = data_dic[key] / sum

        return {
            'ans': {
                'Return': ret,
                'Volatility': vol,
                'SharpRatio': sharp
            },
            'ratio': data_dic
        }, 200



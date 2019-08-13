from flask_restplus import Resource, Namespace, reqparse, fields
import pandas as pd
from init_optmizer import optimizer
import pathlib
from model.recommend_market_fund import get_recom_marker_fund

api = Namespace('allocation', description='根据用户的风险指标和总资产，获得资产分配的比例（浮点数列表）')

fund_model = api.model(
    'fund_model',
    {
        'code': fields.String,
        'symbol': fields.String,
        'fund_type': fields.String,
        'ratio': fields.Float
    }
)

# page_model = api.model(
#     'page_model',
#     {
#         'page': fields.Integer,
#         'page_size': fields.Integer,
#         'total_size': fields.Integer
#     }
# )

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

allocation_model = api.model(
    'allocation',
    {
        'allocation_id': fields.String,
        # 'pagination': fields.Nested(page_model),
        'allocation': fields.List(fields.Nested(fund_model)),
        'ratio': fields.Nested(ration_model),
    }
)
#
# allocation_info_model = api.model(
#     'allocation_info',
#     {
#         'pagination': fields.Nested(page_model),
#         'allocation': fields.List(fields.Nested(fund_model))
#     }
# )

PATH = pathlib.Path(__file__).parent.parent
DATA_PATH = PATH.joinpath("data").resolve()
instruments = pd.read_csv(DATA_PATH.joinpath('instruments.csv'), usecols=['code', 'symbol', 'fund_type'])

# 新增一种配置
_allocation_risk_parser = reqparse.RequestParser()
_allocation_risk_parser.add_argument('risk_index', type=float, help='能够接受的风险', choices=(0.01, 0.02, 0.03, 0.04, 0.05))
_allocation_risk_parser.add_argument('fund_risk', type=int, help='用于筛选的基金风险（5表示全部，默认）', choices=(1, 2, 3, 4, 5),
                                     default=5)


def calculate_ratio(fund_list):
    """计算一个资产配置的各种基金占比"""
    d = dict()
    for fund in fund_list:
        fund_type = fund['fund_type']
        d[fund_type] = d.get(fund_type, 0) + fund['ratio']
    return d


@api.route('/choose')
class AllocatorOnRisk(Resource):

    # @api.response(200, 'allocate successfully', model=allocation_model)
    # @api.expect(_allocation_risk_parser)
    # @api.marshal_list_with(allocation_model)
    @api.expect(_allocation_risk_parser)
    def get(self):
        """
        新建一种资产配置方案
        :param risk, page_size
        :return id, pagination, allocation, ratio
        """
        args = _allocation_risk_parser.parse_args()
        fund_risk = args['fund_risk']
        ret, vol, sr, w = optimizer.get_fixed_ans(fixed='volatility', value=args['risk_index'])
        market_dict, recom_dict, ratio = get_recom_marker_fund(w, sort_by='risk')
        if fund_risk == 1:
            market_dict = [x for x in market_dict if x[1]['fund_risk'] == '中低风险']
        elif fund_risk == 2:
            market_dict = [x for x in market_dict if x[1]['fund_risk'] == '中风险']
        elif fund_risk == 3:
            market_dict = [x for x in market_dict if x[1]['fund_risk'] == '中高风险']
        elif fund_risk == 4:
            market_dict = [x for x in market_dict if x[1]['fund_risk'] == '高风险']
        return {
                   'allocation': market_dict,
               }, 200


_risk_parser = reqparse.RequestParser()
_risk_parser.add_argument('risk_index', type=float, help='能够接受的风险', choices=(0.01, 0.02, 0.03, 0.04, 0.05),
                          required=True)


@api.route('/list')
class List(Resource):
    @api.expect(_risk_parser)
    def get(self):
        """
        新建一种资产配置方案，按权重排序
        :return:
        """
        args = _risk_parser.parse_args()
        ret, vol, sr, w = optimizer.get_fixed_ans(fixed='volatility', value=args['risk_index'])
        market_dict, recom_dict, ratio = get_recom_marker_fund(w, sort_by='risk')
        market_dict = sorted(market_dict, key=lambda x: x[1]['weight'], reverse=True)
        return {
            'allocation': market_dict
        }




@api.route('/recommend')
class Recommend(Resource):
    @api.expect(_risk_parser)
    def get(self):
        """
        获得推荐的基金列表
        :return:
        """
        args = _risk_parser.parse_args()
        ret, vol, sr, w = optimizer.get_fixed_ans(fixed='volatility', value=args['risk_index'])
        market_dict, recom_dict, ratio = get_recom_marker_fund(w, sort_by='risk')
        return {
            'recommend': recom_dict
        }


@api.route('/ratio')
class Ratio(Resource):
    @api.expect(_risk_parser)
    def get(self):
        """
        获得基金分配的比例
        :return:
        """
        args = _risk_parser.parse_args()
        ret, vol, sr, w = optimizer.get_fixed_ans(fixed='volatility', value=args['risk_index'])
        market_dict, recom_dict, ratio = get_recom_marker_fund(w, sort_by='risk')
        return {
            'ratio': ratio
        }

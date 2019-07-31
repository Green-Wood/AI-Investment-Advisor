from flask_restplus import Resource, Namespace, reqparse, fields
import pandas as pd
from db import mongo
from bson.objectid import ObjectId
from bson.errors import InvalidId
from werkzeug.exceptions import NotFound

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

page_model = api.model(
    'page_model',
    {
        'page': fields.Integer,
        'page_size': fields.Integer,
        'total_size': fields.Integer
    }
)

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
        'pagination': fields.Nested(page_model),
        'allocation': fields.List(fields.Nested(fund_model)),
        'ratio': fields.Nested(ration_model)
    }
)

allocation_info_model = api.model(
    'allocation_info',
    {
        'pagination': fields.Nested(page_model),
        'allocation': fields.List(fields.Nested(fund_model))
    }
)

funds = pd.read_csv('funds/instruments.csv', usecols=['code', 'symbol', 'fund_type'])

# 新增一种配置
_allocation_parser = reqparse.RequestParser()
_allocation_parser.add_argument('risk_index', type=float, help='能够接受的风险')
_allocation_parser.add_argument('total_asset', type=float, help='总资产')
_allocation_parser.add_argument('page_size', default=5, type=int, help='一页的大小')


@api.route('')
class Allocator(Resource):

    @staticmethod
    def calculate_ratio(fund_list):
        """计算一个资产配置的各种基金占比"""
        d = dict()
        for fund in fund_list:
            fund_type = fund['fund_type']
            d[fund_type] = d.get(fund_type, 0) + fund['ratio']
        return d

    @api.response(200, 'allocate successfully', model=allocation_model)
    @api.expect(_allocation_parser)
    @api.marshal_list_with(allocation_model)
    def post(self):
        """
        新建一种资产配置方案，并以分页的形式返回
        :param risk, asset, page_size
        :return id, pagination, allocation, ratio
        """
        w = [0.1, 0.2, 0.4, 0.15, 0.15]
        args = _allocation_parser.parse_args()
        page_size = args['page_size']
        fund_list = [
            {
                'code': str(funds.iloc[i, 0]),
                'symbol': str(funds.iloc[i, 1]),
                'fund_type': str(funds.iloc[i, 2]),
                'ratio': w[i]
            }
            for i in range(len(w))
        ]
        ratio = self.calculate_ratio(fund_list)
        allocation_id = mongo.db.allocation.insert_one({'allocation': fund_list}).inserted_id
        return {
                   'allocation_id': allocation_id,
                   'pagination': {
                       'page': 0,
                       'page_size': page_size,
                       'total_size': len(fund_list)
                   },
                   'allocation': fund_list[: page_size],
                   'ratio': ratio
               }, 200


# 从缓存中获得资产配置信息
_allo_info_parser = reqparse.RequestParser()
_allo_info_parser.add_argument('page', required=True, type=int, help='需要第几页')
_allo_info_parser.add_argument('page_size', required=True, type=int, help='一页的大小')


@api.route('/<string:allocation_id>')
@api.doc(params={'allocation_id': '资产分配的id'})
class AllocationInfo(Resource):

    @api.response(200, 'allocate successfully', model=allocation_info_model)
    @api.response(404, 'Allocation id doest not exist')
    @api.expect(_allo_info_parser)
    @api.marshal_list_with(allocation_info_model)
    def get(self, allocation_id):
        """
        通过id获取资产配置方案，以分页的形式返回
        :param allocation_id:
        :return:
        """
        args = _allo_info_parser.parse_args()
        page = args['page']
        page_size = args['page_size']

        try:
            allocation = mongo.db.allocation.find_one({'_id': ObjectId(allocation_id)})
        except InvalidId:
            raise NotFound('Allocation id doest not exist')
        if allocation is None:
            raise NotFound('Allocation id doest not exist')

        fund_list = allocation['allocation']
        return {
                   'pagination': {
                       'page': page,
                       'page_size': page_size,
                       'total_size': len(fund_list)
                   },
                   'allocation': fund_list[page * page_size: (page + 1) * page_size]
               }, 200

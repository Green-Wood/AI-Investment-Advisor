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
allocation_model = api.model(
    'allocation',
    {
        'allocation_id': fields.String,
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

    @api.response(200, 'allocate successfully', model=allocation_model)
    @api.expect(_allocation_parser)
    @api.marshal_list_with(allocation_model)
    def post(self):
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
        allocation_id = mongo.db.allocation.insert_one({'allocation': fund_list}).inserted_id
        return {
                   'allocation_id': allocation_id,
                   'pagination': {
                       'page': 0,
                       'page_size': page_size,
                       'total_size': len(fund_list)
                   },
                   'allocation': fund_list[: page_size]
               }, 200


# 从缓存中获得配置信息
_allo_info_parser = reqparse.RequestParser()
_allo_info_parser.add_argument('page', required=True, type=int, help='需要第几页')
_allo_info_parser.add_argument('page_size', required=True, type=int, help='一页的大小')


@api.route('/<string:allocation_id>')
@api.doc(params={'allocation_id': '资产分配的id'})
class AllocationInfo(Resource):

    @api.response(200, 'allocate successfully', model=allocation_model)
    @api.response(404, 'Allocation id doest not exist')
    @api.expect(_allo_info_parser)
    @api.marshal_list_with(allocation_model)
    def get(self, allocation_id):
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
                   'allocation_id': allocation_id,
                   'pagination': {
                       'page': page,
                       'page_size': page_size,
                       'total_size': len(fund_list)
                   },
                   'allocation': fund_list[page * page_size: (page + 1) * page_size]
               }, 200


from flask_restplus import Resource, Namespace, reqparse, fields
import requests
from os import getenv
import pandas as pd

api = Namespace('allocation', description='根据用户的风险指标和总资产，获得资产分配的比例（浮点数列表）')

_allocation_parser = reqparse.RequestParser()
_allocation_parser.add_argument('risk_index', required=True, type=float)
_allocation_parser.add_argument('total_asset', required=True, type=float)

fund_model = api.model(
    'fund_model',
    {
        'code': fields.Integer,
        'symbol': fields.String,
        'fund_type': fields.String,
        'ratio': fields.Float
    }
)
allocation = api.model(
    'allocation',
    {
        'allocation': fields.List(fields.Nested(fund_model))
    }
)

funds = pd.read_csv('./resources/instruments.csv', usecols=['code', 'symbol', 'fund_type'])
funds_value = funds.values


@api.route('')
class Allocator(Resource):

    @api.response(200, 'allocate successfully', model=allocation)
    @api.expect(_allocation_parser)
    def post(self):
        w = [0.1, 0.2, 0.4, 0.15, 0.15]
        fund_list = [
            {
                'code': funds_value[i, 0],
                'symbol': funds_value[i, 1],
                'fund_type': funds_value[i, 2],
                'ratio': w[i]
            }
            for i in range(len(w))
        ]
        return fund_list


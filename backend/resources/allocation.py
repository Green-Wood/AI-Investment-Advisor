from flask_restplus import Resource, Namespace, reqparse, fields
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

funds = pd.read_csv('funds/instruments.csv', usecols=['code', 'symbol', 'fund_type'])


@api.route('')
class Allocator(Resource):

    @api.response(200, 'allocate successfully', model=allocation)
    @api.expect(_allocation_parser)
    @api.marshal_list_with(fund_model, envelope='allocation')
    def get(self):
        w = [0.1, 0.2, 0.4, 0.15, 0.15]
        fund_list = [
            {
                'code': funds.iloc[i, 0],
                'symbol': funds.iloc[i, 1],
                'fund_type': funds.iloc[i, 2],
                'ratio': w[i]
            }
            for i in range(len(w))
        ]
        return fund_list, 200


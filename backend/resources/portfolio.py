from flask_restplus import Resource, Namespace, reqparse, fields
import pandas as pd
import datetime
from werkzeug.exceptions import NotFound, BadRequest

api = Namespace('portfolio', description='基金的单只和累计收益信息')

_fund_parser = reqparse.RequestParser()

fund_info_model = api.model(
    'fund_info_model',
    {
        'datetime': fields.DateTime,
        'net_value': fields.Float
    }
)

fund_info_list_model = api.model(
    'fund_info_list_model',
    {
        'info_list': fields.List(fields.Nested(fund_info_model))
    }
)


@api.route('/<string:code>')
@api.doc(params={'code': '该基金的代码（字符串）'})
class Allocator(Resource):

    @api.response(200, 'get fund info successfully', model=fund_info_list_model)
    @api.response(404, 'fund not found')
    @api.response(400, 'This fund does not contain net_value, only daily_profit')
    @api.expect(_fund_parser)
    @api.marshal_list_with(fund_info_model, envelope='info_list')
    def get(self, code):
        """
        根据基金代码获取该基金的详细信息
        :param code:
        :return:
        """
        args = _fund_parser.parse_args()
        net_type = args['net_value_type']
        recent_time = args['recent_time']

        code = '0' * (6 - len(code)) + code    # 标准化基金代码

        path = 'data/nav/{dir}/{file}.csv'.format(dir=code[-2:], file=code)
        try:
            fund = pd.read_csv(path, usecols=['datetime', net_type])   # 基金时间转化格式
        except FileNotFoundError:
            raise NotFound('Fund not Found')
        except ValueError:
            raise BadRequest('This fund does not contain net_value, only daily_profit')
        fund['datetime'] = pd.to_datetime(fund['datetime'])

        last_date = fund.iloc[-1, 0]       # 设置时间范围
        if recent_time == 'month':
            time_delta = datetime.timedelta(days=30)
        elif recent_time == 'half year':
            time_delta = datetime.timedelta(days=182)
        else:
            time_delta = datetime.timedelta(days=356)
        date_after = last_date - time_delta
        fund = fund[fund['datetime'] > date_after]

        fund_info_list = [
            {
                'datetime': fund.iloc[i, 0],
                'net_value': fund.iloc[i, 1]
            }
            for i in range(len(fund))
        ]

        return fund_info_list, 200


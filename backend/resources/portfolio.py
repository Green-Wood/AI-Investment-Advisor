from flask_restplus import Resource, Namespace, reqparse, fields
import pandas as pd
import datetime
from werkzeug.exceptions import NotFound, BadRequest
from model.portfolio import get_single_fund_data, get_portfolio_data

api = Namespace('portfolio', description='基金的单只和累计收益信息')

fund_info_model = api.model(
    'single_fund_model',
    {
        'his_x': fields.List(fields.Date),
        'his_y': fields.List(fields.Float),
        'forecast_x': fields.List(fields.Date),
        'lower_y': fields.List(fields.Float),
        'forecast_y': fields.List(fields.Float),
        'upper_y': fields.List(fields.Float)
    }
)

risk_return_model = api.model(
    'risk_return_model',
    {
        'maxdd': fields.Float,
        'sharpe': fields.Float,
        'sortino': fields.Float,
        'calmar': fields.Float
    }
)
performance_model = api.model(
    'performance_model',
    {
        'p_y_r': fields.Float,
        'b_y_r': fields.Float,
        'winrate': fields.Float,
        'payoff': fields.Float,
        'alpha': fields.Float,
        'beta': fields.Float
    }
)

one_model = api.model(
    'one_model',
    {
        'performance': fields.Nested(performance_model),
        'risk/return profile': fields.Nested(risk_return_model)
    }
)

date_model = api.model(
    'date_model',
    {
        'all': fields.Nested(one_model),
        '1': fields.Nested(one_model),
        '3': fields.Nested(one_model),
        '6': fields.Nested(one_model),
        '12': fields.Nested(one_model),
        'ytd': fields.Nested(one_model),
    }
)

best_portfolio_model = api.model(
    'portfolio_model',
    {
        'p_x': fields.List(fields.Date),
        'p_y': fields.List(fields.Float),
        'b_x': fields.List(fields.Date),
        'b_y': fields.List(fields.Float),
        'info': fields.Nested(date_model)
    }
)


@api.route('/<string:code>')
@api.doc(params={'code': '该基金的代码（字符串）'})
class SingleFund(Resource):

    @api.response(200, 'get fund info successfully', model=fund_info_model)
    @api.response(404, 'fund not found')
    @api.response(400, 'This fund does not contain net_value, only daily_profit')
    @api.marshal_list_with(fund_info_model)
    def get(self, code):
        """
        根据基金代码获取该基金的详细信息
        :param code:
        :return:
        """
        his_x, his_y, forecast_x, lower_y, forecast_y, upper_y = get_single_fund_data(code)
        return {
            'his_x': his_x,
            'his_y': his_y,
            'forecast_x': forecast_x,
            'lower_y': lower_y,
            'forecast_y': forecast_y,
            'upper_y': upper_y
        }


@api.route('/best')
class BestPortfolio(Resource):
    def get(self):
        """
        获得最好的组合收益
        :return:
        """
        pass


_fund_list_parser = reqparse.RequestParser()
_fund_list_parser.add_argument('fund_list', type=str, action='append', help='基金code列表', required=True)


@api.route('/user')
class UserPortfolio(Resource):

    @api.marshal_list_with(best_portfolio_model)
    @api.expect(_fund_list_parser)
    def get(self):
        """
        根据代码列表，获得组合的收益图
        :return:
        """
        args = _fund_list_parser.parse_args()
        p_x, p_y, b_x, b_y, info = get_portfolio_data(args['fund_list'])
        return {
            'p_x': p_x,
            'p_y': p_y,
            'b_x': b_x,
            'b_y': b_y,
            'info': info
        }

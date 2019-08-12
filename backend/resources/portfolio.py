from flask_restplus import Resource, Namespace, reqparse, fields
from model.portfolio import get_single_fund_data, get_portfolio_data, best_portfolio, best_portfolio_info

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

best_portfolio_model = api.model(
    'portfolio_model',
    {
        'x': fields.List(fields.Date),
        'p_y': fields.List(fields.Float),
        'b_y': fields.List(fields.Float),
    }
)

best_and_user_model = api.model(
    'best_and_user',
    {
        'x': fields.List(fields.Date),
        'p_y': fields.List(fields.Float),
        'b_y': fields.List(fields.Float),
    }
)

best_info_model = api.model(
    'best_info_model',
    {
        'best_info': fields.Nested(one_model)
    }
)

_code_parser = reqparse.RequestParser()
_code_parser.add_argument('code', type=int, help='单只基金代码code')


@api.route('/single')
class SingleFund(Resource):

    @api.expect(_code_parser)
    @api.response(200, 'get fund info successfully', model=fund_info_model)
    @api.marshal_with(fund_info_model)
    def get(self):
        """
        根据基金代码获取该基金的详细信息
        :param code:
        :return:
        """
        args = _code_parser.parse_args()
        code = args['code']
        code = str(code).zfill(6)
        # try:
        his_x, his_y, forecast_x, lower_y, forecast_y, upper_y = get_single_fund_data(code)
        # except KeyError:
        #     print(code)
        #     raise NotFound('Fund not found')
        return {
            'his_x': his_x[::3],
            'his_y': his_y[::3],
            'forecast_x': forecast_x,
            'lower_y': lower_y,
            'forecast_y': forecast_y,
            'upper_y': upper_y
        }


_best_portfolio_parser = reqparse.RequestParser()
_best_portfolio_parser.add_argument('risk_index', type=float, help='能够接受的风险', choices=(0.01, 0.02, 0.03, 0.04, 0.05))


@api.route('/best')
class BestPortfolio(Resource):
    @api.expect(_best_portfolio_parser)
    @api.marshal_with(best_and_user_model)
    def get(self):
        """
        获得最好的组合收益
        :return:
        """
        args = _best_portfolio_parser.parse_args()
        risk_val = args['risk_index']
        p = best_portfolio['portfolio_{}'.format(risk_val)]
        b = best_portfolio['baseline_{}'.format(risk_val)]
        return {
            'x': best_portfolio['datetime'].values[::2],
            'p_y': p.values[::2],
            'b_y': b.values[::2],
        }


@api.route('/best_info')
class BestInfo(Resource):
    @api.expect(_best_portfolio_parser)
    @api.marshal_with(best_info_model)
    def get(self):
        """
        获得最好的组合的相关信息
        :return:
        """
        args = _best_portfolio_parser.parse_args()
        risk_val = args['risk_index']
        info = best_portfolio_info[str(risk_val)]
        return {
            'best_info': info['all']
        }

#
# @api.route('/user')
# class UserPortfolio(Resource):
#
#     @api.marshal_with(best_portfolio_model)
#     @api.expect(_fund_list_parser)
#     def get(self):
#         """
#         根据代码列表，获得组合的收益图
#         :return:
#         """
#         args = _fund_list_parser.parse_args()
#         fund_list = args['fund_list'].split()
#         p_x, p_y, b_y, info = get_portfolio_data(fund_list)
#         return {
#             'x': p_x,
#             'p_y': p_y,
#             'b_y': b_y,
#             'info': info
#         }

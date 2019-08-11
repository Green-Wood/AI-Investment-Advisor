from flask_restplus import Resource, Namespace, reqparse, fields
from model.efficient_frontier import get_best_ef_data, get_user_ef_data

api = Namespace('ef', description='根据基金代码列表，efficient frontier')

ef_model = api.model(
    'ef_model',
    {
        'best_ret': fields.List(fields.Float),
        'best_vol': fields.List(fields.Float),
        'best_sharp_ratio': fields.List(fields.Float),
        'best_text': fields.List(fields.String),
        'scatter_ret': fields.List(fields.Float),
        'scatter_vol': fields.List(fields.Float),
        'scatter_sharp_ratio': fields.List(fields.Float),
    }
)


_fund_list_parser = reqparse.RequestParser()
_fund_list_parser.add_argument('fund_list', type=str, help='基金code列表(split by space)')


@api.route('/best')
class Best(Resource):
    # @api.marshal_with(ef_model)
    @api.expect(_fund_list_parser)
    def get(self):
        """
        返回最佳的ef曲线，以及散点
        :param code:
        :return:
        """
        args = _fund_list_parser.parse_args()
        if args['fund_list'] is None:
            user_frontier, user_text, user_data = (None, None, None), None, None
        else:
            fund_list = args['fund_list'].split()
            user_frontier, user_text, user_data = get_user_ef_data(fund_list)
        best_frontier, text, best_data = get_best_ef_data()
        return {
            'best_ret': best_frontier[0],
            'best_vol': best_frontier[1],
            'best_sharp_ratio': best_frontier[2],
            'best_text': text,
            'scatter_ret': best_data[1],
            'scatter_vol': best_data[0],
            'scatter_sharp_ratio': best_data[2],
            'user_ret': user_frontier[0],
            'user_vol': user_frontier[1],
            'user_sharp_ratio': user_frontier[2],
            'user_text': user_text
        }


@api.route('/user')
class User(Resource):
    @api.expect(_fund_list_parser)
    @api.marshal_with(ef_model)
    def get(self):
        """
        根据基金列表返回ef曲线，以及散点
        :return:
        """
        args = _fund_list_parser.parse_args()
        fund_list = args['fund_list'].split()
        choose_frontier, text, choose_data = get_user_ef_data(fund_list)
        return {
            'line_ret': choose_frontier[0],
            'line_vol': choose_frontier[1],
            'line_sharp_ratio': choose_frontier[2],
            'line_text': text,
            'scatter_ret': choose_data[0],
            'scatter_vol': choose_data[1],
            'scatter_sharp_ratio': choose_data[2],
        }
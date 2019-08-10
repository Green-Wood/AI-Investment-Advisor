from flask_restplus import Resource, Namespace, reqparse, fields
from model.efficient_frontier import get_best_ef_data, get_user_ef_data

api = Namespace('ef', description='根据基金代码列表，efficient frontier')

ef_model = api.model(
    'ef_model',
    {
        'line_ret': fields.List(fields.Float),
        'line_vol': fields.List(fields.Float),
        'line_sharp_ratio': fields.List(fields.Float),
        'line_text': fields.List(fields.String),
        'scatter_ret': fields.List(fields.Float),
        'scatter_vol': fields.List(fields.Float),
        'scatter_sharp_ratio': fields.List(fields.Float),
    }
)


@api.route('/best')
class Best(Resource):
    @api.marshal_with(ef_model)
    def get(self):
        """
        返回最佳的ef曲线，以及散点
        :param code:
        :return:
        """
        best_frontier, text, best_data = get_best_ef_data()
        return {
            'line_ret': best_frontier[0],
            'line_vol': best_frontier[1],
            'line_sharp_ratio': best_frontier[2],
            'line_text': text,
            'scatter_ret': best_data[1],
            'scatter_vol': best_data[0],
            'scatter_sharp_ratio': best_data[2],
        }


_fund_list_parser = reqparse.RequestParser()
_fund_list_parser.add_argument('fund_list', type=str, help='基金code列表(split by space)')


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
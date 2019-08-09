from flask_restplus import Resource, Namespace, reqparse, fields
from model.efficient_frontier import get_best_ef_data, get_user_ef_data

api = Namespace('ef', description='根据基金代码列表，得到相关系数矩阵')

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
    def get(self):
        """
        返回最佳的ef曲线
        :param code:
        :return:
        """
        best_frontier, text, best_data = get_best_ef_data()
        return {
            'line_ret': best_frontier[0],
            'line_vol': best_frontier[1],
            'line_sharp_ratio': best_frontier[2],
            'line_text': text,
            'scatter_ret': best_data[0],
            'scatter_vol': best_data[1],
            'scatter_sharp_ratio': best_data[2],
        }


_ef_parser = reqparse.RequestParser()
_ef_parser.add_argument('fund_list', type=str, action='append', help='基金code列表')


@api.route('/user')
class User(Resource):
    def get(self):
        """
        根据基金列表返回ef曲线
        :return:
        """
        args = _ef_parser.parse_args()
        choose_frontier, text, choose_data = get_user_ef_data(args['fund_list'])
        return {
            'line_ret': choose_frontier[0],
            'line_vol': choose_frontier[1],
            'line_sharp_ratio': choose_frontier[2],
            'line_text': text,
            'scatter_ret': choose_data[0],
            'scatter_vol': choose_data[1],
            'scatter_sharp_ratio': choose_data[2],
        }
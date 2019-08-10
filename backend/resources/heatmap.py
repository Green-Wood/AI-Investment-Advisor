from flask_restplus import Resource, Namespace, reqparse, fields
from model.corr_map import get_corr
import json
from werkzeug.exceptions import NotFound
from resources.efficient_frontier import _fund_list_parser

api = Namespace('heatmap', description='根据基金代码列表，得到相关系数矩阵')


@api.route('/choose')
class HeatMap(Resource):
    @api.expect(_fund_list_parser)
    def get(self):
        """
        根据基金代码列表，得到相关系数矩阵
        :param code:
        :return:
        """
        args = _fund_list_parser.parse_args()
        fund_list = args['fund_list'].split()
        try:
            json_str = get_corr(fund_list).to_json(orient='index')
        except KeyError:
            raise NotFound('Fund not find')
        return json.loads(json_str)

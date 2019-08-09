from flask_restplus import Resource, Namespace, reqparse, fields
from model.corr_map import get_corr
import json

api = Namespace('heatmap', description='根据基金代码列表，得到相关系数矩阵')

_heatmap_parser = reqparse.RequestParser()
_heatmap_parser.add_argument('fund_list', type=str, action='append', help='基金code列表')


@api.route('')
class HeatMap(Resource):
    def get(self):
        """
        根据基金代码获取该基金的详细信息（一个月、半年、一年）
        :param code:
        :return:
        """
        args = _heatmap_parser.parse_args()
        fund_list = args['fund_list']
        json_str = get_corr(fund_list).to_json(orient='index')
        return json.loads(json_str)



from flask_restplus import Resource, Namespace, reqparse, fields
from model.corr_map import get_corr
import json
from werkzeug.exceptions import NotFound
from resources.efficient_frontier import _fund_list_parser
from init_optmizer import optimizer

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


_risk_parser = reqparse.RequestParser()
_risk_parser.add_argument('risk_index', type=float, help='能够接受的风险', choices=(0.01, 0.02, 0.03, 0.04, 0.05),
                          required=True)


@api.route('/risk')
class BasedOnRisk(Resource):
    @api.expect(_risk_parser)
    def get(self):
        """
        根据风险值，得到相关系数矩阵，10只weight最高的基金
        :return:
        """
        args = _risk_parser.parse_args()
        ret, vol, sr, w = optimizer.get_fixed_ans(fixed='volatility', value=args['risk_index'])
        fund_list = [x[0] for x in sorted(w.items(), key=lambda x: x[1], reverse=True)[:10]]
        json_str = get_corr(fund_list).to_json(orient='index')
        return json.loads(json_str)
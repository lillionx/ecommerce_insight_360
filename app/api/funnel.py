"""
E-Commerce Insight 360 - 用户漏斗API接口
项目: 电商全链路数据洞察平台
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

from app.api.assistant_func import unified_response
from app.services import funnel_service

bp = Blueprint('funnel', __name__)


# @bp.route('/funnel', methods=['GET'])
# def get_funnel_data():
#     """
#     获取用户漏斗数据
#
#     Query Parameters:
#         - date: 统计日期 (YYYY-MM-DD)，默认为当天
#
#     Returns:
#         JSON: 用户漏斗数据
#     """
#     try:
#         start_day = request.args.get('start_date', datetime.now().strftime('%Y-%m-%d'))
#         end_day = request.args.get('end_date')
#         if end_day is not None:
#             end_day = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
#         # 验证日期格式
#         try:
#             datetime.strptime(start_day, '%Y-%m-%d')
#             if end_day is not None:
#                 datetime.strptime(end_day, '%Y-%m-%d')
#         except ValueError:
#             return jsonify({
#                 'code': 400,
#                 'message': 'Invalid date format',
#                 'error': 'Date format should be YYYY-MM-DD'
#             }), 400
#
#         # 调用业务逻辑
#         data = funnel_service.get_funnel_data(start_day,end_day)
#
#         return jsonify({
#             'code': 200,
#             'message': 'success',
#             'data': data,
#             'timestamp': int(datetime.now().timestamp())
#         })
#
#     except Exception as e:
#         return jsonify({
#             'code': 500,
#             'message': 'Internal Server Error',
#             'error': str(e)
#         }), 500

@bp.route('/funnel', methods=['GET'])
@unified_response
def get_funnel_data():
    start_day = request.args.get('start_date', datetime.now().strftime('%Y-%m-%d'))
    end_day = request.args.get('end_date')
    data = funnel_service.get_funnel_data(start_day, end_day)
    return jsonify(data)
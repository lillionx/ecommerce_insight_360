"""
E-Commerce Insight 360 - 用户分析API接口
项目: 电商全链路数据洞察平台
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

import app.services.user_daily
from app.services import user_service
from app.services import user_daily
from app.api.assistant_func import unified_response

bp = Blueprint('users', __name__)


@bp.route('/users', methods=['GET'])
def get_user_analysis():
    """
    获取用户分析数据

    Query Parameters:
        - date: 统计日期 (YYYY-MM-DD)，默认为当天

    Returns:
        JSON: 用户分析数据
    """
    try:
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

        # 验证日期格式
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'code': 400,
                'message': 'Invalid date format',
                'error': 'Date format should be YYYY-MM-DD'
            }), 400

        # 调用业务逻辑
        data = user_service.get_user_analysis(date)

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': data,
            'timestamp': int(datetime.now().timestamp())
        })

    except Exception as e:
        return jsonify({
            'code': 500,
            'message': 'Internal Server Error',
            'error': str(e)
        }), 500


@bp.route('/users/rfm', methods=['GET'])
def get_user_rfm():
    """
    获取用户RFM分层数据

    Query Parameters:
        - date: 统计日期 (YYYY-MM-DD)

    Returns:
        JSON: RFM分层数据
    """
    try:
        date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))

        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'code': 400,
                'message': 'Invalid date format',
                'error': 'Date format should be YYYY-MM-DD'
            }), 400

        data = user_service.get_rfm_distribution(date)

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': data,
            'timestamp': int(datetime.now().timestamp())
        })

    except Exception as e:
        return jsonify({
            'code': 500,
            'message': 'Internal Server Error',
            'error': str(e)
        }), 500


@bp.route('/users/daily', methods=['GET'])
@unified_response
def get_user_daily():
    date = request.args.get('date', datetime.now().strftime('%Y-%m-%d'))
    data= app.services.user_daily.get_user_daily(date)
    return jsonify(data)


@bp.route('/users/period', methods=['GET'])
@unified_response
def get_user_overall():
    start_date = request.args.get('start_date', datetime.now().strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    data = app.services.user_daily.get_user_overall(start_date, end_date)
    return jsonify(data)
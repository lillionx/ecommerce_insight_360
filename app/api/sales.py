"""
E-Commerce Insight 360 - 销售大盘API接口
项目: 电商全链路数据洞察平台
"""
from encodings import undefined

from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

from app.api.assistant_func import unified_response
from app.models.database import execute_query
from app.services import sales_service

bp = Blueprint('sales', __name__)


@bp.route('/sales', methods=['GET'])
def get_sales_summary():
    """
    获取销售大盘数据

    Query Parameters:
        - start_date: 开始日期 (YYYY-MM-DD)
        - end_date: 结束日期 (YYYY-MM-DD)

    Returns:
        JSON: 销售汇总数据
    """
    try:
        # 获取请求参数
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # 设置默认日期范围
        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        # 验证日期格式
        try:
            datetime.strptime(start_date, '%Y-%m-%d')
            datetime.strptime(end_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'code': 400,
                'message': 'Invalid date format',
                'error': 'Date format should be YYYY-MM-DD'
            }), 400

        # 调用业务逻辑
        data = sales_service.get_sales_summary(start_date, end_date)

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


@bp.route('/sales/trend', methods=['GET'])
def get_sales_trend():
    """
    获取销售趋势数据

    Query Parameters:
        - start_date: 开始日期
        - end_date: 结束日期

    Returns:
        JSON: 销售趋势数据
    """
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date:
            start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        if not end_date:
            end_date = datetime.now().strftime('%Y-%m-%d')

        data = sales_service.get_sales_trend(start_date, end_date)

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


@bp.route('/sales/hourly', methods=['GET'])
#@unified_response
def get_hourly_sales():
    """
    获取小时级别销售数据

    Query Parameters:
        - date: 统计日期 (YYYY-MM-DD)

    Returns:
        JSON: 小时销售数据
    """
    try:
        date = request.args.get('date')

        if not date:
            date = datetime.now().strftime('%Y-%m-%d')

        # 验证日期格式
        try:
            datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'code': 400,
                'message': 'Invalid date format',
                'error': 'Date format should be YYYY-MM-DD'
            }), 400

        data = sales_service.get_hourly_sales(date)

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
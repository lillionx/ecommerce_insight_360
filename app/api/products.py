"""
E-Commerce Insight 360 - 商品分析API接口
项目: 电商全链路数据洞察平台
"""

from flask import Blueprint, request, jsonify
from datetime import datetime

from flask import render_template

from sqlalchemy.orm import undefer

from app.api.assistant_func import unified_response
from app.services import product_service
from app.services.product_service import get_orders_by_date

bp = Blueprint('products', __name__)


@bp.route('/products', methods=['GET'])
#@unified_response
def get_product_rank():
    """
    获取商品销售排行数据

    Query Parameters:
        - date: 统计日期 (YYYY-MM-DD)，默认为当天
        - rank_by: 排行依据 (quantity/amount)，默认为quantity

    Returns:
        JSON: 商品排行数据
    """
    try:
        start_day = request.args.get('start_date', datetime.now().strftime('%Y-%m-%d'))
        end_day = request.args.get('end_date')
        rank_by = request.args.get('rank_by', 'quantity')
        if end_day is not None:
            end_day = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
        # 验证日期格式
        try:
            datetime.strptime(start_day, '%Y-%m-%d')
            if end_day is not None:
                datetime.strptime(end_day, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'code': 400,
                'message': 'Invalid date format',
                'error': 'Date format should be YYYY-MM-DD'
            }), 400

        # 验证rank_by参数
        if rank_by not in ['quantity', 'amount']:
            return jsonify({
                'code': 400,
                'message': 'Invalid rank_by parameter',
                'error': 'rank_by should be quantity or amount'
            }), 400

        # 调用业务逻辑
        data = product_service.get_product_rank(start_day,end_day, rank_by)

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


@bp.route('/products/category', methods=['GET'])
def get_category_distribution():
    """
    获取商品类目销售分布

    Query Parameters:
        - date: 统计日期 (YYYY-MM-DD)

    Returns:
        JSON: 类目销售分布数据
    """
    try:
        start_day = request.args.get('start_date', datetime.now().strftime('%Y-%m-%d'))
        end_day = request.args.get('end_date')

        try:
            datetime.strptime(start_day, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'code': 400,
                'message': 'Invalid date format',
                'error': 'Date format should be YYYY-MM-DD'
            }), 400

        data = product_service.get_category_distribution(start_day,end_day)

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


@bp.route('/products/details', methods=['GET'])
@unified_response
def get_product_details():
    product_id = request.args.get('product_id', type=int)
    data = product_service.get_product_details(product_id)
    return jsonify(data)


@bp.route('/products/orders', methods=['GET'])
@unified_response
def orders_api():
    date = request.args.get('date')
    status = request.args.get('status', None)  # 可选参数

    orders = get_orders_by_date(date, status)

    return jsonify(orders)
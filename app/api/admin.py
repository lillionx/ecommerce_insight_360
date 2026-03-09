"""
E-Commerce Insight 360 - 管理API接口
项目: 电商全链路数据洞察平台
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
from app.services import etl_service

bp = Blueprint('admin', __name__)


@bp.route('/etl/run', methods=['POST'])
def run_etl():
    """
    触发ETL任务执行

    Request Body:
        - data_date: 数据日期 (YYYY-MM-DD)，默认为当天

    Returns:
        JSON: ETL执行结果
    """
    try:
        data = request.get_json() or {}
        data_date = data.get('date', datetime.now().strftime('%Y-%m-%d'))

        # 验证日期格式
        try:
            datetime.strptime(data_date, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'code': 400,
                'message': 'Invalid date format',
                'error': 'Date format should be YYYY-MM-DD'
            }), 400

        # 执行ETL任务
        result = etl_service.run_etl_pipeline(data_date)

        return jsonify({
            'code': 200,
            'message': 'success',
            'data': result,
            'timestamp': int(datetime.now().timestamp())
        })

    except Exception as e:
        return jsonify({
            'code': 500,
            'message': 'Internal Server Error',
            'error': str(e)
        }), 500


@bp.route('/health', methods=['GET'])
def health_check():
    """
    健康检查接口

    Returns:
        JSON: 服务状态
    """
    return jsonify({
        'code': 200,
        'message': 'success',
        'data': {
            'status': 'healthy',
            'timestamp': int(datetime.now().timestamp())
        }
    })

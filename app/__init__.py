"""
E-Commerce Insight 360 - Flask应用工厂
项目: 电商全链路数据洞察平台
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from app.config import get_config

# 初始化SQLAlchemy
db = SQLAlchemy()


def create_app(config_name=None):
    """
    Flask应用工厂函数

    Args:
        config_name: 配置环境名称

    Returns:
        Flask应用实例
    """
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    app = Flask(__name__)

    # 加载配置
    config_obj = get_config(config_name)
    app.config.from_object(config_obj)

    # 初始化SQLAlchemy
    db.init_app(app)

    # 配置日志
    setup_logging(app)

    # 注册蓝图
    register_blueprints(app)

    # 注册错误处理器
    register_error_handlers(app)

    # 创建数据库表
    with app.app_context():
        db.create_all()

    return app


def setup_logging(app):
    """配置应用日志"""
    if not app.debug:
        # 日志目录
        log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 文件处理器
        log_file = os.path.join(log_dir, 'ecommerce_insight.log')
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10240000,
            backupCount=10,
            encoding='utf-8'
        )

        # 日志格式
        formatter = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('E-Commerce Insight 360 启动')


def register_blueprints(app):
    """注册Flask蓝图"""
    from app.api import sales, funnel, products, users, admin

    app.register_blueprint(sales.bp, url_prefix='/api/stats')
    app.register_blueprint(funnel.bp, url_prefix='/api/stats')
    app.register_blueprint(products.bp, url_prefix='/api/stats')
    app.register_blueprint(users.bp, url_prefix='/api/stats')
    app.register_blueprint(admin.bp, url_prefix='/api/admin')


def register_error_handlers(app):
    """注册全局错误处理器"""

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'code': 400,
            'message': 'Bad Request',
            'error': str(error)
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'code': 404,
            'message': 'Not Found',
            'error': str(error)
        }), 404

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f'Server Error: {str(error)}')
        return jsonify({
            'code': 500,
            'message': 'Internal Server Error',
            'error': 'Please contact administrator'
        }), 500

    @app.errorhandler( Exception)
    def handle_exception(error):
        app.logger.error(f'Unhandled Exception: {str(error)}')
        return jsonify({
            'code': 500,
            'message': 'Internal Server Error',
            'error': str(error)
        }), 500

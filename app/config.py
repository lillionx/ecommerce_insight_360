"""
E-Commerce Insight 360 - 配置文件
项目: 电商全链路数据洞察平台
"""

import os
from datetime import timedelta

# mysql8.0中执行  CREATE DATABASE ecommerce_insight CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
class Config:
    """基础配置类"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-2026-ecommerce'

    # 数据库类型选择 (sqlite/mysql)
    DATABASE_TYPE = os.environ.get('DATABASE_TYPE', 'mysql')

    # SQLite配置
    SQLITE_DB_PATH = os.environ.get('SQLITE_DB_PATH', os.path.join(os.path.dirname(os.path.dirname(__file__)), 'ecommerce_insight.db'))

    # MySQL数据库配置
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '123456')
    MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'ecommerce_insight')

    # 根据数据库类型构建连接URI
    if DATABASE_TYPE == 'sqlite':
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{SQLITE_DB_PATH}"
    else:
        SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"

    # SQLAlchemy配置
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_SIZE = 10
    SQLALCHEMY_MAX_OVERFLOW = 20
    SQLALCHEMY_POOL_RECYCLE = 3600
    SQLALCHEMY_ECHO = False

    # Pandas配置
    PANDAS_MODE = os.environ.get('PANDAS_MODE', 'pyarrow')
    PANDAS_COPY_ON_WRITE = True
    PANDAS_DEFAULT_dtype = 'pyarrow'

    # Flask配置
    JSON_AS_ASCII = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    JSON_SORT_KEYS = False

    # 分页配置
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

    # 时区配置
    TIMEZONE = 'Asia/Shanghai'


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False


class TestingConfig(Config):
    """测试环境配置"""
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URI',
        'mysql+pymysql://root:password@localhost/ecommerce_insight_test'
    )


# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}


def get_config(env=None):
    """获取配置对象"""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'default')
    return config.get(env, DevelopmentConfig)

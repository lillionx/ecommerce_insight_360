"""
E-Commerce Insight 360 - 数据库连接管理
项目: 电商全链路数据洞察平台
"""

import pymysql
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, scoped_session
from app.config import get_config
import os


def get_database_connection():
    """
    获取数据库连接（用于原生SQL查询）

    Returns:
        pymysql连接对象
    """
    config = get_config(os.environ.get('FLASK_ENV', 'development'))

    connection = pymysql.connect(
        host=config.MYSQL_HOST,
        port=config.MYSQL_PORT,
        user=config.MYSQL_USER,
        password=config.MYSQL_PASSWORD,
        database=config.MYSQL_DATABASE,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


def get_sqlalchemy_engine():
    """
    获取SQLAlchemy引擎（用于pandas直接查询）

    Returns:
        SQLAlchemy引擎对象
    """
    config = get_config(os.environ.get('FLASK_ENV', 'development'))
    engine = create_engine(
        config.SQLALCHEMY_DATABASE_URI,
        pool_size=config.SQLALCHEMY_POOL_SIZE,
        max_overflow=config.SQLALCHEMY_MAX_OVERFLOW,
        pool_recycle=config.SQLALCHEMY_POOL_RECYCLE,
        echo=config.SQLALCHEMY_ECHO
    )
    return engine


def get_db_session():
    """
    获取数据库会话（用于SQLAlchemy ORM操作）

    Returns:
        作用域会话对象
    """
    engine = get_sqlalchemy_engine()
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)


def execute_query(sql, params=None):
    """
    执行查询SQL

    Args:
        sql: SQL语句
        params: 参数元组

    Returns:
        查询结果列表
    """
    connection = get_database_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, params or ())
            results = cursor.fetchall()
            return results
    finally:
        connection.close()


def execute_update(sql, params=None):
    """
    执行更新SQL

    Args:
        sql: SQL语句
        params: 参数元组

    Returns:
        影响的行数
    """
    connection = get_database_connection()
    try:
        with connection.cursor() as cursor:
            affected_rows = cursor.execute(sql, params or ())
            connection.commit()
            return affected_rows
    finally:
        connection.close()


def execute_many(sql, params_list):
    """
    批量执行SQL

    Args:
        sql: SQL语句
        params_list: 参数列表

    Returns:
        影响的行数
    """
    connection = get_database_connection()
    try:
        with connection.cursor() as cursor:
            affected_rows = cursor.executemany(sql, params_list)
            connection.commit()
            return affected_rows
    finally:
        connection.close()

"""
E-Commerce Insight 360 - ETL服务
项目: 电商全链路数据洞察平台
"""

import pandas as pd
from datetime import datetime
from app.models.database import execute_query, execute_update
import os
import sys

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


def run_etl_pipeline(data_date: str) -> dict:
    """
    执行完整ETL流程

    Args:
        data_date: 数据日期

    Returns:
        ETL执行结果
    """
    result = {
        'status': 'success',
        'data_date': data_date,
        'steps': [],
        'start_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'end_time': None,
        'duration': None,
        'error': None
    }

    try:
        # Step 1: 导入原始数据
        result['steps'].append(import_raw_data(data_date))

        # Step 2: 计算汇总数据
        result['steps'].append(calculate_daily_sales(data_date))

        # Step 3: 计算商品排行
        result['steps'].append(calculate_product_rank(data_date))

        # Step 4: 计算用户RFM
        result['steps'].append(calculate_user_rfm(data_date))

        result['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    except Exception as e:
        result['status'] = 'failed'
        result['error'] = str(e)

    return result


def import_raw_data(data_date: str) -> dict:
    """
    导入原始数据到数据库

    Args:
        data_date: 数据日期

    Returns:
        导入结果
    """
    step_result = {'step': 'import_raw_data', 'status': 'success'}

    try:
        # 读取CSV文件
        data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                                'data_pipeline', 'raw_data')

        # 导入订单数据
        orders_file = os.path.join(data_dir, 'orders.csv')
        if os.path.exists(orders_file):
            orders_df = pd.read_csv(orders_file)
            orders_df['create_time'] = pd.to_datetime(orders_df['create_time'])
            orders_df['pay_time'] = pd.to_datetime(orders_df['pay_time'], errors='coerce')

            # 清理数据
            orders_df = orders_df.drop_duplicates(subset=['order_id'])
            orders_df['amount'] = pd.to_numeric(orders_df['amount'], errors='coerce').fillna(0)
            orders_df = orders_df[orders_df['amount'] >= 0]

            # 批量插入（简化处理）
            for _, row in orders_df.iterrows():
                sql = """
                    INSERT IGNORE INTO fact_orders
                    (order_id, user_id, product_id, amount, quantity, status, create_time, pay_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """
                execute_update(sql, (
                    int(row['order_id']),
                    int(row['user_id']),
                    int(row['product_id']),
                    float(row['amount']),
                    int(row.get('quantity', 1)),
                    str(row.get('status', 'pending')),
                    row['create_time'].strftime('%Y-%m-%d %H:%M:%S') if pd.notna(row['create_time']) else None,
                    row['pay_time'].strftime('%Y-%m-%d %H:%M:%S') if pd.notna(row['pay_time']) else None
                ))

            step_result['records_imported'] = len(orders_df)

        return step_result

    except Exception as e:
        step_result['status'] = 'failed'
        step_result['error'] = str(e)
        return step_result


def calculate_daily_sales(data_date: str) -> dict:
    """
    计算每日销售汇总

    Args:
        data_date: 统计日期

    Returns:
        计算结果
    """
    step_result = {'step': 'calculate_daily_sales', 'status': 'success'}

    try:
        sql = """
            INSERT INTO ads_daily_sales
            (stat_date, gmv, total_orders, paid_orders, unit_price, user_count)
            SELECT
                DATE(%s) as stat_date,
                COALESCE(SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END), 0) as gmv,
                COUNT(DISTINCT order_id) as total_orders,
                COUNT(DISTINCT CASE WHEN status = 'paid' THEN order_id END) as paid_orders,
                COALESCE(SUM(CASE WHEN status = 'paid' THEN amount ELSE 0 END), 0) /
                    NULLIF(COUNT(DISTINCT CASE WHEN status = 'paid' THEN order_id END), 0) as unit_price,
                COUNT(DISTINCT user_id) as user_count
            FROM fact_orders
            WHERE DATE(create_time) = DATE(%s)
            AND status != 'cancelled'
            ON DUPLICATE KEY UPDATE
                gmv = VALUES(gmv),
                total_orders = VALUES(total_orders),
                paid_orders = VALUES(paid_orders),
                unit_price = VALUES(unit_price),
                user_count = VALUES(user_count),
                update_time = NOW()
        """

        execute_update(sql, (data_date, data_date))
        step_result['date'] = data_date

        return step_result

    except Exception as e:
        step_result['status'] = 'failed'
        step_result['error'] = str(e)
        return step_result


def calculate_product_rank(data_date: str) -> dict:
    """
    计算商品销售排行

    Args:
        data_date: 统计日期

    Returns:
        计算结果
    """
    step_result = {'step': 'calculate_product_rank', 'status': 'success'}

    try:
        sql = """
            INSERT INTO ads_product_rank
            (stat_date, product_id, product_name, category, sales_quantity, sales_amount, rank_by_quantity, rank_by_amount)
            SELECT
                DATE(%s) as stat_date,
                p.product_id,
                p.product_name,
                p.category,
                COALESCE(SUM(o.quantity), 0) as sales_quantity,
                COALESCE(SUM(o.amount), 0) as sales_amount,
                ROW_NUMBER() OVER (ORDER BY SUM(o.quantity) DESC) as rank_by_quantity,
                ROW_NUMBER() OVER (ORDER BY SUM(o.amount) DESC) as rank_by_amount
            FROM dim_products p
            LEFT JOIN fact_orders o ON p.product_id = o.product_id
                AND DATE(o.create_time) = DATE(%s)
                AND o.status = 'paid'
            GROUP BY p.product_id, p.product_name, p.category
            ON DUPLICATE KEY UPDATE
                sales_quantity = VALUES(sales_quantity),
                sales_amount = VALUES(sales_amount),
                rank_by_quantity = VALUES(rank_by_quantity),
                rank_by_amount = VALUES(rank_by_amount),
                update_time = NOW()
        """

        execute_update(sql, (data_date, data_date))
        step_result['date'] = data_date

        return step_result

    except Exception as e:
        step_result['status'] = 'failed'
        step_result['error'] = str(e)
        return step_result


def calculate_user_rfm(data_date: str) -> dict:
    """
    计算用户RFM分层

    Args:
        data_date: 统计日期

    Returns:
        计算结果
    """
    step_result = {'step': 'calculate_user_rfm', 'status': 'success'}

    try:
        # 简化的RFM计算
        sql = """
            INSERT INTO ads_user_rfm
            (user_id, recency, frequency, monetary, rfm_score, user_level, stat_date)
            SELECT
                user_id,
                DATEDIFF(DATE(%s), MAX(DATE(create_time))) as recency,
                COUNT(*) as frequency,
                SUM(amount) as monetary,
                '' as rfm_score,
                CASE
                    WHEN SUM(amount) > 5000 AND COUNT(*) > 10 THEN 'high_value'
                    WHEN DATEDIFF(DATE(%s), MAX(DATE(create_time))) <= 30 THEN 'new'
                    WHEN DATEDIFF(DATE(%s), MAX(DATE(create_time))) > 90 THEN 'churn'
                    WHEN SUM(amount) > 1000 THEN 'medium_value'
                    ELSE 'low_value'
                END as user_level,
                DATE(%s) as stat_date
            FROM fact_orders
            WHERE status = 'paid'
            GROUP BY user_id
            ON DUPLICATE KEY UPDATE
                recency = VALUES(recency),
                frequency = VALUES(frequency),
                monetary = VALUES(monetary),
                rfm_score = VALUES(rfm_score),
                user_level = VALUES(user_level),
                update_time = NOW()
        """

        execute_update(sql, (data_date, data_date, data_date, data_date))
        step_result['date'] = data_date

        return step_result

    except Exception as e:
        step_result['status'] = 'failed'
        step_result['error'] = str(e)
        return step_result

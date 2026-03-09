"""
E-Commerce Insight 360 - 销售大盘业务逻辑
项目: 电商全链路数据洞察平台
"""

from datetime import datetime, timedelta
from sqlalchemy import func, case
from app import db
from app.models import FactOrders, AdsDailySales


def get_sales_summary(start_date: str, end_date: str) -> dict:
    """
    获取销售汇总数据

    Args:
        start_date: 开始日期
        end_date: 结束日期

    Returns:
        销售汇总字典
    """
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)

        # 使用SQLAlchemy查询
        result = db.session.query(
            func.sum(FactOrders.amount).label('gmv'),
            func.count(FactOrders.order_id).label('total_orders'),
            func.sum(case((FactOrders.status == 'paid', 1), else_=0)).label('paid_orders'),
            func.count(func.distinct(FactOrders.user_id)).label('user_count')
        ).filter(
            FactOrders.create_time >= start_dt,
            FactOrders.create_time < end_dt,
            FactOrders.status != 'cancelled'
        ).first()

        gmv = float(result.gmv or 0)
        paid_orders = int(result.paid_orders or 0)
        total_orders = int(result.total_orders or 0)
        user_count = int(result.user_count or 0)
        unit_price = round(gmv / paid_orders, 2) if paid_orders > 0 else 0

        return {
            'gmv': gmv,
            'total_orders': total_orders,
            'paid_orders': paid_orders,
            'unit_price': unit_price,
            'user_count': user_count
        }
    except Exception as e:
        print(f"Error in get_sales_summary: {e}")
        return {
            'gmv': 0,
            'total_orders': 0,
            'paid_orders': 0,
            'unit_price': 0,
            'user_count': 0
        }


def get_sales_trend(start_date: str, end_date: str) -> dict:
    """
    获取销售趋势数据

    Args:
        start_date: 开始日期
        end_date: 结束日期

    Returns:
        销售趋势列表
    """
    try:
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_dt = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)

        results = db.session.query(
            func.date(FactOrders.create_time).label('stat_date'),
            func.sum(FactOrders.amount).label('gmv'),
            func.count(FactOrders.order_id).label('orders')
        ).filter(
            FactOrders.create_time >= start_dt,
            FactOrders.create_time < end_dt,
            FactOrders.status != 'cancelled'
        ).group_by(
            func.date(FactOrders.create_time)
        ).order_by(
            func.date(FactOrders.create_time)
        ).all()

        trend = []
        for row in results:
            trend.append({
                'date': row.stat_date.strftime('%Y-%m-%d') if row.stat_date else None,
                'gmv': float(row.gmv or 0),
                'orders': int(row.orders or 0)
            })

        return {'trend': trend}
    except Exception as e:
        print(f"Error in get_sales_trend: {e}")
        return {'trend': []}


def get_hourly_sales(date: str) -> dict:
    """
    获取小时级别销售数据

    Args:
        date: 统计日期

    Returns:
        小时销售数据列表
    """
    try:
        date_dt = datetime.strptime(date, '%Y-%m-%d')
        next_day = date_dt + timedelta(days=1)

        results = db.session.query(
            func.extract('hour', FactOrders.create_time).label('hour'),
            func.sum(FactOrders.amount).label('gmv'),
            func.count(FactOrders.order_id).label('orders')
        ).filter(
            FactOrders.create_time >= date_dt,
            FactOrders.create_time < next_day,
            FactOrders.status == 'paid'
        ).group_by(
            func.extract('hour', FactOrders.create_time)
        ).order_by(
            func.extract('hour', FactOrders.create_time)
        ).all()

        hourly_data = []
        for row in results:
            hourly_data.append({
                'hour': int(row.hour or 0),
                'gmv': float(row.gmv or 0),
                'orders': int(row.orders or 0)
            })

        return {'hourly': hourly_data}
    except Exception as e:
        print(f"Error in get_hourly_sales: {e}")
        return {'hourly': []}

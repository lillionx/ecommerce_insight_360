"""
E-Commerce Insight 360 - 商品分析业务逻辑
项目: 电商全链路数据洞察平台
"""

from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.sql.coercions import expect

from app import db
from app.models import DimProducts, FactOrders


def get_product_rank(start_date: str,end_date:str,rank_by: str = 'quantity') -> dict:
    """
    获取商品销售排行数据

    Args:
        date: 统计日期
        rank_by: 排行依据 (quantity/amount)

    Returns:
        商品排行数据
    """
    try:
        start_day = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date is None:
            end_day = start_day + timedelta(days=1)
        else:
            end_day = datetime.strptime(end_date, '%Y-%m-%d')

        # 使用SQLAlchemy查询
        results = db.session.query(
            DimProducts.product_id,
            DimProducts.product_name,
            DimProducts.category,
            #coalesce,空值替代，前面一个位置的结果未空时，用后面不为空的值进行替代
            func.coalesce(func.sum(FactOrders.quantity), 0).label('sales_quantity'),
            func.coalesce(func.sum(FactOrders.amount), 0).label('sales_amount')
        ).outerjoin(
            FactOrders,
            db.and_(
                DimProducts.product_id == FactOrders.product_id,
                FactOrders.create_time >= start_day,
                FactOrders.create_time < end_day,
                FactOrders.status == 'paid'
            )
        ).group_by(
            DimProducts.product_id,
            DimProducts.product_name,
            DimProducts.category
        ).having(
            db.or_(
                func.coalesce(func.sum(FactOrders.quantity), 0) > 0,
                func.coalesce(func.sum(FactOrders.amount), 0) > 0
            )
        )

        if rank_by == 'quantity':
            results = results.order_by(func.coalesce(func.sum(FactOrders.quantity), 0).desc())
        else:
            results = results.order_by(func.coalesce(func.sum(FactOrders.amount), 0).desc())

        results = results.limit(10).all()

        top10 = []
        for idx, row in enumerate(results, 1):
            top10.append({
                'rank': idx,
                'product_id': row.product_id,
                'product_name': row.product_name,
                'category': row.category,
                'sales_quantity': int(row.sales_quantity or 0),
                'sales_amount': float(row.sales_amount or 0)
            })

        return {'top10': top10}
    except Exception as e:
        print(f"Error in get_product_rank: {e}")
        return {'top10': []}


def get_category_distribution(start_date: str,end_date:str) -> dict:
    """
    获取商品类目销售分布

    Args:
        date: 统计日期

    Returns:
        类目销售分布数据
    """
    try:
        start_day = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date is None:
            end_day = start_day + timedelta(days=1)
        else:
            end_day = datetime.strptime(end_date, '%Y-%m-%d')

        results = db.session.query(
            DimProducts.category,
            func.coalesce(func.sum(FactOrders.amount), 0).label('sales_amount'),
            func.count(func.distinct(FactOrders.order_id)).label('order_count')
        ).outerjoin(
            FactOrders,
            db.and_(
                DimProducts.product_id == FactOrders.product_id,
                FactOrders.create_time >= start_day,
                FactOrders.create_time < end_day,
                FactOrders.status == 'paid'
            )
        ).group_by(
            DimProducts.category
        ).having(
            func.coalesce(func.sum(FactOrders.amount), 0) > 0
        ).order_by(
            func.coalesce(func.sum(FactOrders.amount), 0).desc()
        ).all()

        # 计算总销售额
        total_amount = sum(float(row.sales_amount or 0) for row in results)

        distribution = []
        for row in results:
            sales_amount = float(row.sales_amount or 0)
            percentage = round(sales_amount / total_amount * 100, 2) if total_amount > 0 else 0

            distribution.append({
                'category': row.category,
                'sales_amount': sales_amount,
                'order_count': int(row.order_count or 0),
                'percentage': percentage
            })

        return {'distribution': distribution}
    except Exception as e:
        print(f"Error in get_category_distribution: {e}")
        return {'distribution': []}


def get_product_details(product_id: int) -> dict:
    """
    获取商品详情

    Args:
        product_id: 商品ID

    Returns:
        商品详情
    """
    try:
        product = db.session.get(DimProducts, product_id)

        if not product:
            return None

        return {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'category': product.category,
            'price': float(product.price or 0),
            'stock': product.stock
        }
    except Exception as e:
        print(f"Error in get_product_details: {e}")
        return None



def get_orders_by_date(date_str, status=None):
    """
    根据日期和可选状态查询订单
    返回 (orders_list, error_message)
    """
    try:
        selected_date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except Exception as e:
        print(f"Error in get_orders_by_date: {e}")
        return None
    try:
        # 基础查询：按创建日期过滤
        query = FactOrders.query.filter(func.date(FactOrders.create_time) == selected_date)

        if status:
            query = query.filter(FactOrders.status == status)

        orders = query.all()

        # 转换为字典列表
        result = []
        for order in orders:
            result.append({
                'order_id': order.order_id,
                'user_id': order.user_id,
                'product_id': order.product_id,
                'amount': float(order.amount) if order.amount else 0,
                'quantity': order.quantity,
                'status': order.status,
                'create_time': order.create_time.isoformat() if order.create_time else None,
                'pay_time': order.pay_time.isoformat() if order.pay_time else None,
            })
        return {'result':result}
    except Exception as e:
        print(f"Error in get_orders_by_date: {e}")
        return None


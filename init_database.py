"""
E-Commerce Insight 360 - 数据库初始化脚本 (SQLite版本)
项目: 电商全链路数据洞察平台
"""

import os
import sys
import random
from datetime import datetime, timedelta

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app, db
from app.models import DimUsers, DimProducts, FactOrders, FactEvents, AdsDailySales, AdsProductRank, AdsUserRfm


def create_sample_data():
    """生成样例数据"""
    print("正在生成样例数据...")

    # 清空现有数据
    db.drop_all()
    db.create_all()

    # 插入样例用户数据
    cities = ['北京', '上海', '广州', '深圳', '杭州', '成都', '武汉', '西安', '南京', '重庆']
    genders = ['M', 'F']

    users = []
    for i in range(1, 101):
        user = DimUsers(
            user_id=i,
            username=f'user_{i:03d}',
            gender=random.choice(genders),
            age=random.randint(18, 60),
            city=random.choice(cities),
            register_time=datetime.now() - timedelta(days=random.randint(1, 365))
        )
        users.append(user)

    db.session.bulk_save_objects(users)
    print(f"  已生成 {len(users)} 条用户数据")

    # 插入样例商品数据
    categories = ['电子产品', '服装', '食品', '家居', '图书', '运动', '美妆', '玩具']
    product_names = [
        'iPhone 15 Pro', 'MacBook Pro', 'AirPods Pro', 'iPad Pro',
        'HUAWEI Mate 60', '小米手机', 'OPPO Find X',
        'Nike运动T恤', 'Adidas运动鞋', '优衣库牛仔裤', 'ZARA连衣裙', '海澜之家外套',
        '坚果礼盒', '零食大礼包', '有机牛奶', '咖啡豆', '茶叶礼盒',
        '实木沙发', '办公桌', '床品四件套', '吸尘器', '电饭煲',
        'Python编程', '数据结构与算法', '人文社科图书', '小说套装',
        '瑜伽垫', '跑步机', '篮球', '泳镜', '羽毛球拍',
        '护肤套装', '口红', '香水', '面膜', '洗面奶',
        '积木玩具', '遥控汽车', '毛绒玩具', '芭比娃娃'
    ]

    products = []
    for i, name in enumerate(product_names, 1):
        product = DimProducts(
            product_id=i,
            product_name=name,
            category=categories[i % len(categories)],
            price=round(random.uniform(50, 10000), 2),
            stock=random.randint(0, 1000)
        )
        products.append(product)

    db.session.bulk_save_objects(products)
    print(f"  已生成 {len(products)} 条商品数据")

    # 插入样例订单数据
    statuses = ['pending', 'paid', 'shipped', 'delivered', 'cancelled']
    paid_statuses = ['paid', 'shipped', 'delivered']

    orders = []
    for i in range(1, 1001):
        user_id = random.randint(1, 100)
        product_id = random.randint(1, len(product_names))
        amount = round(random.uniform(50, 5000), 2)
        quantity = random.randint(1, 5)
        status = random.choice(statuses)
        create_time = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))

        pay_time = None
        if status in paid_statuses:
            pay_time = create_time + timedelta(hours=random.randint(1, 48))

        order = FactOrders(
            order_id=i,
            user_id=user_id,
            product_id=product_id,
            amount=amount,
            quantity=quantity,
            status=status,
            create_time=create_time,
            pay_time=pay_time
        )
        orders.append(order)

    db.session.bulk_save_objects(orders)
    print(f"  已生成 {len(orders)} 条订单数据")

    # 插入样例事件数据
    event_types = ['view', 'cart', 'wishlist', 'checkout', 'review']
    device_types = ['mobile', 'desktop', 'tablet']

    events = []
    for i in range(1, 2001):
        user_id = random.randint(1, 100)
        product_id = random.randint(1, len(product_names))
        event_type = random.choice(event_types)
        session_id = f'session_{random.randint(1, 500)}'
        device_type = random.choice(device_types)
        create_time = datetime.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))

        event = FactEvents(
            event_id=i,
            user_id=user_id,
            product_id=product_id,
            event_type=event_type,
            session_id=session_id,
            device_type=device_type,
            create_time=create_time
        )
        events.append(event)

    db.session.bulk_save_objects(events)
    print(f"  已生成 {len(events)} 条事件数据")

    db.session.commit()

    # 计算汇总数据
    calculate_aggregate_data()

    print("样例数据生成成功！")


def calculate_aggregate_data():
    """计算汇总数据"""
    print("正在计算汇总数据...")

    # 计算每日销售汇总
    today = datetime.now().date()

    paid_orders = FactOrders.query.filter_by(status='paid').all()

    total_gmv = sum(float(o.amount) for o in paid_orders)
    total_orders = FactOrders.query.count()
    paid_order_count = len(paid_orders)
    unit_price = total_gmv / paid_order_count if paid_order_count > 0 else 0
    user_count = len(set(o.user_id for o in paid_orders))

    daily_sales = AdsDailySales(
        stat_date=today,
        gmv=total_gmv,
        total_orders=total_orders,
        paid_orders=paid_order_count,
        unit_price=unit_price,
        user_count=user_count
    )
    db.session.add(daily_sales)

    # 计算商品排行
    from sqlalchemy import func

    product_sales = db.session.query(
        FactOrders.product_id,
        func.sum(FactOrders.quantity).label('sales_quantity'),
        func.sum(FactOrders.amount).label('sales_amount')
    ).filter(
        FactOrders.status == 'paid'
    ).group_by(FactOrders.product_id).all()

    # 按销量排序
    product_sales_sorted = sorted(product_sales, key=lambda x: x.sales_quantity or 0, reverse=True)[:10]

    for rank, ps in enumerate(product_sales_sorted, 1):
        product = DimProducts.query.get(ps.product_id)
        if product:
            product_rank = AdsProductRank(
                stat_date=today,
                product_id=product.product_id,
                product_name=product.product_name,
                category=product.category,
                sales_quantity=int(ps.sales_quantity or 0),
                sales_amount=float(ps.sales_amount or 0),
                rank_by_quantity=rank,
                rank_by_amount=rank
            )
            db.session.add(product_rank)

    # 计算用户RFM
    user_stats = db.session.query(
        FactOrders.user_id,
        func.max(FactOrders.create_time).label('last_order_date'),
        func.count(FactOrders.order_id).label('order_count'),
        func.sum(FactOrders.amount).label('total_amount')
    ).filter(
        FactOrders.status == 'paid'
    ).group_by(FactOrders.user_id).all()

    for us in user_stats:
        recency = (datetime.now() - us.last_order_date).days if us.last_order_date else 999
        frequency = us.order_count or 0
        monetary = float(us.total_amount or 0)

        # 简单的用户分层逻辑
        if monetary > 5000 and frequency > 10:
            user_level = 'high_value'
        elif recency <= 30:
            user_level = 'new'
        elif recency > 90:
            user_level = 'churn'
        elif monetary > 1000:
            user_level = 'medium_value'
        else:
            user_level = 'low_value'

        rfm = AdsUserRfm(
            user_id=us.user_id,
            recency=recency,
            frequency=frequency,
            monetary=monetary,
            rfm_score='',
            user_level=user_level,
            stat_date=today
        )
        db.session.add(rfm)

    db.session.commit()
    print("汇总数据计算完成！")


def main():
    """主函数"""
    print("=" * 60)
    print("E-Commerce Insight 360 - 数据库初始化 (SQLite)")
    print("=" * 60)

    # 创建Flask应用
    app = create_app('development')

    with app.app_context():
        # 创建数据库表
        print("正在创建数据库表...")
        db.create_all()
        print("数据库表创建成功")

        # 生成样例数据
        create_sample_data()

        print("=" * 60)
        print("数据库初始化完成！")
        print("=" * 60)


if __name__ == '__main__':
    main()

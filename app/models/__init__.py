"""
E-Commerce Insight 360 - 数据库模型
项目: 电商全链路数据洞察平台
"""

from datetime import datetime
from app import db
import sqlalchemy as sa


class DimUsers(db.Model):
    """用户维度表"""
    __tablename__ = 'dim_users'

    user_id = db.Column(db.Integer, primary_key=True, comment='用户ID')
    username = db.Column(db.String(50), nullable=False, comment='用户名')
    gender = db.Column(db.String(1), default='U', comment='性别')
    age = db.Column(db.Integer, comment='年龄')
    city = db.Column(db.String(50), comment='城市')
    register_time = db.Column(db.DateTime, nullable=False, comment='注册时间')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='记录创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='记录更新时间')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'gender': self.gender,
            'age': self.age,
            'city': self.city,
            'register_time': self.register_time.strftime('%Y-%m-%d %H:%M:%S') if self.register_time else None
        }


class DimProducts(db.Model):
    """商品维度表"""
    __tablename__ = 'dim_products'

    product_id = db.Column(db.Integer, primary_key=True, comment='商品ID')
    product_name = db.Column(db.String(200), nullable=False, comment='商品名称')
    category = db.Column(db.String(50), nullable=False, comment='商品类目')
    price = db.Column(db.Numeric(19, 2), nullable=False, comment='商品单价')
    stock = db.Column(db.Integer, default=0, comment='库存数量')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='记录创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='记录更新时间')

    def to_dict(self):
        return {
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category': self.category,
            'price': float(self.price) if self.price else 0,
            'stock': self.stock
        }


class FactOrders(db.Model):
    """订单事实表"""
    __tablename__ = 'fact_orders'

    order_id = db.Column(db.BigInteger, primary_key=True, comment='订单ID')
    user_id = db.Column(db.Integer, nullable=False, index=True, comment='用户ID')
    product_id = db.Column(db.Integer, nullable=False, index=True, comment='商品ID')
    amount = db.Column(db.Numeric(19, 2), nullable=False, comment='订单金额')
    quantity = db.Column(db.Integer, default=1, comment='购买数量')
    status = db.Column(db.String(20), nullable=False, default='pending', comment='订单状态')
    create_time = db.Column(db.DateTime, nullable=False, index=True, comment='订单创建时间')
    pay_time = db.Column(db.DateTime, comment='支付时间')
    create_time_record = db.Column(db.DateTime, default=datetime.now, comment='记录创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='记录更新时间')

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'amount': float(self.amount) if self.amount else 0,
            'quantity': self.quantity,
            'status': self.status,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None,
            'pay_time': self.pay_time.strftime('%Y-%m-%d %H:%M:%S') if self.pay_time else None
        }


class FactEvents(db.Model):
    """用户行为事实表"""
    __tablename__ = 'fact_events'

    event_id = db.Column(db.BigInteger, primary_key=True, comment='事件ID')
    user_id = db.Column(db.Integer, nullable=False, index=True, comment='用户ID')
    product_id = db.Column(db.Integer, index=True, comment='商品ID')
    event_type = db.Column(db.String(20), nullable=False, comment='事件类型')
    session_id = db.Column(db.String(50), comment='会话ID')
    device_type = db.Column(db.String(20), comment='设备类型')
    create_time = db.Column(db.DateTime, nullable=False, index=True, comment='事件发生时间')
    create_time_record = db.Column(db.DateTime, default=datetime.now, comment='记录创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='记录更新时间')

    def to_dict(self):
        return {
            'event_id': self.event_id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'event_type': self.event_type,
            'session_id': self.session_id,
            'device_type': self.device_type,
            'create_time': self.create_time.strftime('%Y-%m-%d %H:%M:%S') if self.create_time else None
        }


class AdsDailySales(db.Model):
    """每日销售汇总表"""
    __tablename__ = 'ads_daily_sales'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键')
    stat_date = db.Column(db.Date, nullable=False, unique=True, comment='统计日期')
    gmv = db.Column(db.Numeric(19, 2), nullable=False, default=0, comment='当日GMV')
    total_orders = db.Column(db.Integer, nullable=False, default=0, comment='当日订单数')
    paid_orders = db.Column(db.Integer, nullable=False, default=0, comment='当日已支付订单数')
    unit_price = db.Column(db.Numeric(19, 2), nullable=False, default=0, comment='当日客单价')
    user_count = db.Column(db.Integer, nullable=False, default=0, comment='当日下单用户数')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='记录创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='记录更新时间')

    def to_dict(self):
        return {
            'stat_date': self.stat_date.strftime('%Y-%m-%d') if self.stat_date else None,
            'gmv': float(self.gmv) if self.gmv else 0,
            'total_orders': self.total_orders,
            'paid_orders': self.paid_orders,
            'unit_price': float(self.unit_price) if self.unit_price else 0,
            'user_count': self.user_count
        }


class AdsProductRank(db.Model):
    """商品销售排行表"""
    __tablename__ = 'ads_product_rank'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键')
    stat_date = db.Column(db.Date, nullable=False, comment='统计日期')
    product_id = db.Column(db.Integer, nullable=False, comment='商品ID')
    product_name = db.Column(db.String(200), comment='商品名称')
    category = db.Column(db.String(50), comment='商品类目')
    sales_quantity = db.Column(db.Integer, nullable=False, default=0, comment='销售数量')
    sales_amount = db.Column(db.Numeric(19, 2), nullable=False, default=0, comment='销售金额')
    rank_by_quantity = db.Column(db.Integer, comment='按销量排名')
    rank_by_amount = db.Column(db.Integer, comment='按金额排名')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='记录创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='记录更新时间')

    def to_dict(self):
        return {
            'stat_date': self.stat_date.strftime('%Y-%m-%d') if self.stat_date else None,
            'product_id': self.product_id,
            'product_name': self.product_name,
            'category': self.category,
            'sales_quantity': self.sales_quantity,
            'sales_amount': float(self.sales_amount) if self.sales_amount else 0,
            'rank_by_quantity': self.rank_by_quantity,
            'rank_by_amount': self.rank_by_amount
        }


class AdsUserRfm(db.Model):
    """用户RFM分层表"""
    __tablename__ = 'ads_user_rfm'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键')
    user_id = db.Column(db.Integer, nullable=False, comment='用户ID')
    recency = db.Column(db.Integer, comment='R值：距离上次购买天数')
    frequency = db.Column(db.Integer, comment='F值：购买次数')
    monetary = db.Column(db.Numeric(19, 2), comment='M值：总消费金额')
    rfm_score = db.Column(db.String(10), comment='RFM综合得分')
    user_level = db.Column(db.String(20), nullable=False, comment='用户分层')
    stat_date = db.Column(db.Date, nullable=False, comment='统计日期')
    create_time = db.Column(db.DateTime, default=datetime.now, comment='记录创建时间')
    update_time = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, comment='记录更新时间')

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'recency': self.recency,
            'frequency': self.frequency,
            'monetary': float(self.monetary) if self.monetary else 0,
            'rfm_score': self.rfm_score,
            'user_level': self.user_level,
            'stat_date': self.stat_date.strftime('%Y-%m-%d') if self.stat_date else None
        }

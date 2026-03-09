from datetime import datetime, timedelta
from app import create_app, db
from app.models import DimUsers, DimProducts, FactOrders, FactEvents, AdsDailySales, AdsProductRank, AdsUserRfm
from sqlalchemy import func
def get_rfm(date:str):
    date_dt = datetime.strptime(date, '%Y-%m-%d')
    user_stats = db.session.query(
        FactOrders.user_id,
        func.max(FactOrders.create_time).label('last_order_date'),
        func.count(FactOrders.order_id).label('order_count'),
        func.sum(FactOrders.amount).label('total_amount')
    ).filter(
        FactOrders.status == 'paid',
        FactOrders.create_time < date_dt
    ).group_by(FactOrders.user_id).all()

    for us in user_stats:
        recency = (date_dt - us.last_order_date).days if us.last_order_date else 999
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
            stat_date=date_dt
        )
        db.session.add(rfm)

    db.session.commit()
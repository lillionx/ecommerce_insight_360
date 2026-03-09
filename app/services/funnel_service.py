"""
E-Commerce Insight 360 - 用户漏斗业务逻辑
项目: 电商全链路数据洞察平台
"""

from datetime import datetime, timedelta
from sqlalchemy import func
from app import db
from app.models import FactEvents


def get_funnel_data(start_date: str,end_date:str) -> dict:
    start_day = datetime.strptime(start_date, '%Y-%m-%d')
    if end_date is None:
        end_day = start_day + timedelta(days=1)
    else:
        end_day = datetime.strptime(end_date, '%Y-%m-%d')


    stages = [
        (['view', 'review', 'wishlist'], '浏览'),
        (['cart'], '购物车'),
        (['checkout'], '下单')
    ]

    funnel_data = []
    prev_count = None

    for event_types, stage_name in stages:
        # 查询在指定日期内，事件类型在 event_types 中的独立用户数
        query = db.session.query(
            func.count(func.distinct(FactEvents.user_id)).label('count')
        ).filter(
            FactEvents.event_type.in_(event_types),
            FactEvents.create_time >= start_day,
            FactEvents.create_time < end_day
        )
        result = query.first()
        count = int(result.count or 0) if result else 0

        if prev_count is None:
            conversion_rate = 100.0
        else:
            conversion_rate = round(count / prev_count * 100, 2) if prev_count > 0 else 0

        funnel_data.append({
            'stage': stage_name,
            'count': count,
            'conversion_rate': conversion_rate
        })
        prev_count = count

    return {'funnel': funnel_data}


def get_funnel_by_source(date: str) -> dict:
    """
    按来源设备获取漏斗数据

    Args:
        date: 统计日期

    Returns:
        来源设备漏斗数据
    """
    try:
        date_dt = datetime.strptime(date, '%Y-%m-%d')
        next_day = date_dt + timedelta(days=1)

        results = db.session.query(
            FactEvents.device_type,
            FactEvents.event_type,
            func.count(func.distinct(FactEvents.user_id)).label('count')
        ).filter(
            FactEvents.create_time >= date_dt,
            FactEvents.create_time < next_day
        ).group_by(
            FactEvents.device_type,
            FactEvents.event_type
        ).all()

        # 按设备类型分组
        device_funnel = {}
        for row in results:
            device = row.device_type or 'unknown'
            event = row.event_type
            count = int(row.count or 0)

            if device not in device_funnel:
                device_funnel[device] = {}

            device_funnel[device][event] = count

    except Exception as e:
        print(f"Error in get_funnel_by_source: {e}")
        device_funnel = {}

    return {'device_funnel': device_funnel}

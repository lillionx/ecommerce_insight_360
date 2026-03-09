"""
E-Commerce Insight 360 - 用户分析业务逻辑
项目: 电商全链路数据洞察平台
"""

from datetime import datetime, timedelta
from sqlalchemy import func, case
from app import db
from app.models import DimUsers, AdsUserRfm, FactOrders
from app.services import get_rfm


def get_user_analysis(date: str) -> dict:
    """
    获取用户分析综合数据

    Args:
        date: 统计日期

    Returns:
        用户分析数据
    """
    rfm_data = get_rfm_distribution(date)
    gender_data = get_gender_distribution()
    age_data = get_age_distribution()

    return {
        'rfm_distribution': rfm_data.get('rfm_distribution', []),
        'gender_distribution': gender_data.get('gender_distribution', []),
        'age_distribution': age_data.get('age_distribution', [])
    }


def get_rfm_distribution(date: str) -> dict:
    """
    获取用户RFM分层分布

    Args:
        date: 统计日期

    Returns:
        RFM分层数据
    """
    try:
        date_dt = datetime.strptime(date, '%Y-%m-%d')
        #查询输入日期是否有数据
        existing_record = db.session.query(AdsUserRfm).filter(
            AdsUserRfm.stat_date == date_dt
        ).first()

        if not existing_record:
            get_rfm.get_rfm(date)


        results = db.session.query(
            AdsUserRfm.user_level,
            func.count(AdsUserRfm.id).label('count')
        ).filter(
            AdsUserRfm.stat_date == date_dt.date()
        ).group_by(
            AdsUserRfm.user_level
        ).all()

        # 计算总用户数
        total = sum(int(row.count or 0) for row in results)

        rfm_distribution = []
        for row in results:
            count = int(row.count or 0)
            percentage = round(count / total * 100, 2) if total > 0 else 0

            rfm_distribution.append({
                'level': row.user_level,
                'count': count,
                'percentage': percentage
            })

        return {'rfm_distribution': rfm_distribution}
    except Exception as e:
        print(f"Error in get_rfm_distribution: {e}")
        return {'rfm_distribution': []}


def get_gender_distribution() -> dict:
    """
    获取用户性别分布

    Returns:
        性别分布数据
    """
    try:
        results = db.session.query(
            DimUsers.gender,
            func.count(DimUsers.user_id).label('count')
        ).group_by(
            DimUsers.gender
        ).all()

        # 计算总用户数
        total = sum(int(row.count or 0) for row in results)

        gender_distribution = []
        gender_map = {'M': '男性', 'F': '女性', 'U': '未知'}

        for row in results:
            count = int(row.count or 0)
            percentage = round(count / total * 100, 2) if total > 0 else 0

            gender_distribution.append({
                'gender': gender_map.get(row.gender, '未知'),
                'count': count,
                'percentage': percentage
            })

        return {'gender_distribution': gender_distribution}
    except Exception as e:
        print(f"Error in get_gender_distribution: {e}")
        return {'gender_distribution': []}


def get_age_distribution() -> dict:
    """
    获取用户年龄分布

    Returns:
        年龄分布数据
    """
    try:
        # 使用case进行年龄分段
        age_case = case(
            (DimUsers.age < 18, '18岁以下'),
            (DimUsers.age.between(18, 24), '18-25岁'),
            (DimUsers.age.between(25, 34), '26-35岁'),
            (DimUsers.age.between(35, 44), '36-45岁'),
            (DimUsers.age.between(45, 54), '46-55岁'),
            else_='55岁以上'
        )

        results = db.session.query(
            age_case.label('age_range'),
            func.count(DimUsers.user_id).label('count')
        ).filter(
            DimUsers.age.isnot(None)
        ).group_by(
            age_case
        ).all()

        age_distribution = []
        for row in results:
            age_distribution.append({
                'age_range': row.age_range,
                'count': int(row.count or 0)
            })

        return {'age_distribution': age_distribution}
    except Exception as e:
        print(f"Error in get_age_distribution: {e}")
        return {'age_distribution': []}


def get_city_distribution() -> dict:
    """
    获取用户城市分布

    Returns:
        城市分布数据
    """
    try:
        results = db.session.query(
            DimUsers.city,
            func.count(DimUsers.user_id).label('count')
        ).filter(
            DimUsers.city.isnot(None)
        ).group_by(
            DimUsers.city
        ).order_by(
            func.count(DimUsers.user_id).desc()
        ).limit(20).all()

        city_distribution = []
        for row in results:
            city_distribution.append({
                'city': row.city,
                'count': int(row.count or 0)
            })

        return {'city_distribution': city_distribution}
    except Exception as e:
        print(f"Error in get_city_distribution: {e}")
        return {'city_distribution': []}


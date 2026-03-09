from datetime import datetime
from sqlalchemy import func
from app import db
from app.models import DimUsers, AdsUserRfm,FactOrders
from app.services import get_rfm
from typing import TypedDict,List
from collections import Counter

class UserInfo(TypedDict):
    user_id: int
    gender: str
    age: int
    city: str
    leve: str

def get_user_daily(date_str: str) -> dict:
    """
    根据日期获取用户数据，返回字典格式

    Args:
        date_str: 日期字符串，格式为 'YYYY-MM-DD'

    Returns:
        包含用户id、性别、年龄、城市、RFM统计的字典列表
    """
    try:
        date_dt= datetime.strptime(date_str, '%Y-%m-%d').date()
        # 判断是否添加RFM表格内容
        existing_record = db.session.query(AdsUserRfm).filter(
            AdsUserRfm.stat_date == date_dt
        ).first()

        if not existing_record:
            get_rfm.get_rfm(date_str)
        #日期查询
        result = db.session.query(
            FactOrders.user_id,
            DimUsers.gender,
            DimUsers.age,
            DimUsers.city,
            AdsUserRfm.user_level
        ).join(
            DimUsers, FactOrders.user_id == DimUsers.user_id
        ).join(
            AdsUserRfm, FactOrders.user_id == AdsUserRfm.user_id, isouter=True
        ).filter(
            # 将create_time转换为日期与目标日期比较
            func.date(FactOrders.create_time) == date_dt
        ).distinct(
            FactOrders.user_id
        ).all()

        rfm_data = get_rfm_distribution(result)
        gender_data = get_gender_distribution(result)
        age_data = get_age_distribution(result)
        city_data = get_city_distribution(result)

        return {
            'rfm_distribution': rfm_data.get('rfm_distribution', []),
            'gender_distribution': gender_data.get('gender_distribution', []),
            'age_distribution': age_data.get('age_distribution', []),
            'city_distribution': city_data.get('city_distribution', [])
        }
    except Exception as e:
        print(f"Error in get_user_daily: {e}")
        return {'user_daily': []}


def get_rfm_distribution(result: List[UserInfo]) -> dict:
    """
        获取用户RFM分层分布

        Returns:
            RFM分层数据
        """
    try:
        level_counter = Counter()
        for row in result:
            # 获取user_level，处理None值
            if hasattr(row, 'user_level'):
                user_level = row.user_level
            elif isinstance(row, (tuple, list)) and len(row) > 4:
                user_level = row[4]
            else:
                user_level = None

            # 如果user_level为None，归类为'unknown'
            if user_level is None:
                level_counter['unknown'] += 1
            else:
                level_counter[user_level] += 1

            # 计算总用户数
        total_users = len(result)

        # 构建结果列表
        rfm_distribution = []
        for level, count in level_counter.items():
            percentage = round((count / total_users) * 100, 2) if total_users > 0 else 0
            rfm_distribution.append({
                'level': level,
                'count': count,
                'percentage': percentage
            })

        # 按等级排序（可选，可以按字母顺序或自定义顺序）
        rfm_distribution.sort(key=lambda x: x['percentage'])

        return {'rfm_distribution': rfm_distribution}
    except Exception as e:
        print(f"Error in get_rfm_distribution: {e}")
        return {'rfm_distribution': []}

def get_gender_distribution(result: List[UserInfo]) -> dict:
    """
    获取用户性别分布

    Returns:
        性别分布数据
    """
    try:
        gender_counter = Counter()
        gender_map = {'M': '男性', 'F': '女性', 'U': '未知'}

        for row in result:
            # 获取gender
            if hasattr(row, 'gender'):
                gender_code = row.gender
            elif isinstance(row, (tuple, list)) and len(row) > 1:
                gender_code = row[1]  # gender通常在第二个位置
            else:
                gender_code = 'U'  # 默认为未知

            # 处理None值
            if gender_code is None:
                gender_code = 'U'

            # 统计
            gender_counter[gender_code] += 1

        # 计算总人数
        total_users = len(result)

        # 构建结果列表
        gender_distribution = []
        for gender_code, count in gender_counter.items():
            percentage = round((count / total_users) * 100, 2) if total_users > 0 else 0

            gender_distribution.append({
                'gender': gender_map.get(gender_code, '未知'),
                'count': count,
                'percentage': percentage
            })

        # 按常见顺序排序：男性、女性、未知
        gender_order = {'男性': 1, '女性': 2, '未知': 3}
        gender_distribution.sort(key=lambda x: gender_order.get(x['gender'], 4))

        return {'gender_distribution': gender_distribution}
    except Exception as e:
        print(f"Error in get_gender_distribution: {e}")
        return {'gender_distribution': []}

def get_age_distribution(result: List[UserInfo]) -> dict:
    """
    获取用户年龄分布

    Returns:
        年龄分布数据
    """
    try:
        # 定义年龄分段
        age_groups = [
            (lambda age: age < 18, '18岁以下'),
            (lambda age: 18 <= age <= 24, '18-24岁'),
            (lambda age: 25 <= age <= 34, '25-34岁'),
            (lambda age: 35 <= age <= 44, '35-44岁'),
            (lambda age: 45 <= age <= 54, '45-54岁'),
            (lambda age: age >= 55, '55岁及以上')
        ]

        # 统计各年龄段数量
        age_group_counter = Counter()

        for row in result:
            # 获取age
            if hasattr(row, 'age'):
                age = row.age
            elif isinstance(row, (tuple, list)) and len(row) > 2:
                age = row[2]  # age通常在第三个位置
            else:
                age = None

            # 处理None值
            if age is None:
                age_group_counter['年龄未知'] += 1
                continue

            # 确定年龄段
            assigned = False
            for condition, group_name in age_groups:
                if condition(age):
                    age_group_counter[group_name] += 1
                    assigned = True
                    break

            # 如果没有匹配到任何条件，归为未知
            if not assigned:
                age_group_counter['年龄未知'] += 1

        # 计算总人数
        total_users = len(result)

        # 构建结果列表
        age_distribution = []
        for age_group, count in age_group_counter.items():
            percentage = round((count / total_users) * 100, 2) if total_users > 0 else 0
            age_distribution.append({
                'age_group': age_group,
                'count': count,
                'percentage': percentage
            })

        # 按年龄段顺序排序
        age_order = {
            '18岁以下': 1,
            '18-24岁': 2,
            '25-34岁': 3,
            '35-44岁': 4,
            '45-54岁': 5,
            '55岁及以上': 6,
            '年龄未知': 7
        }
        age_distribution.sort(key=lambda x: age_order.get(x['age_group'], 8))

        return {'age_distribution': age_distribution}
    except Exception as e:
        print(f"Error in get_age_distribution: {e}")
        return {'age_distribution': []}

def get_city_distribution(result: List[UserInfo]) -> dict:
    """
    获取用户城市分布

    Returns:
        城市分布数据
    """
    try:
        city_counter = Counter()

        for row in result:
            # 获取city
            if hasattr(row, 'city'):
                city = row.city
            elif isinstance(row, (tuple, list)) and len(row) > 3:
                city = row[3]  # city通常在第四个位置
            else:
                city = None

            # 处理None值和空字符串
            if city is None or city == '':
                city = '未知'

            city_counter[city] += 1

        # 计算总人数
        total_users = len(result)

        # 构建结果列表
        city_distribution = []

        # 按城市出现次数从高到低排序
        for city, count in city_counter.most_common():
            percentage = round((count / total_users) * 100, 2) if total_users > 0 else 0
            city_distribution.append({
                'city': city,
                'count': count,
                'percentage': percentage
            })

        return {'city_distribution': city_distribution}
    except Exception as e:
        print(f"Error in get_city_distribution: {e}")
        return {'city_distribution': []}

def get_user_overall(start_date=None, end_date=None):
    """
    根据日期范围获取用户数据分布（RFM、性别、年龄、城市）
    如果 start_date 和 end_date 均为 None，则查询所有历史数据
    """
    try:
        # 基础查询：关联用户、订单和RFM表
        query = db.session.query(
            DimUsers.gender,
            DimUsers.age,
            DimUsers.city,
            AdsUserRfm.user_level
        ).join(
            FactOrders, DimUsers.user_id == FactOrders.user_id
        ).join(
            AdsUserRfm, DimUsers.user_id == AdsUserRfm.user_id, isouter=True
        ).distinct(DimUsers.user_id)

        if start_date and end_date:
            start_dt = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_dt = datetime.strptime(end_date, '%Y-%m-%d').date()
            query = query.filter(
                func.date(FactOrders.create_time) >= start_dt,
                func.date(FactOrders.create_time) <= end_dt
            )

        result = query.all()

        # 计算分布（假设已有这些辅助函数）
        rfm_data = get_rfm_distribution(result)
        gender_data = get_gender_distribution(result)
        age_data = get_age_distribution(result)
        city_data = get_city_distribution(result)

        return {
            'rfm_distribution': rfm_data.get('rfm_distribution', []),
            'gender_distribution': gender_data.get('gender_distribution', []),
            'age_distribution': age_data.get('age_distribution', []),
            'city_distribution': city_data.get('city_distribution', [])
        }
    except Exception as e:
        print(f"Error in get_user_overall: {e}")
        return {}

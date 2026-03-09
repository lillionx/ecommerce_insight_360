from datetime import datetime
from functools import wraps
from flask import jsonify

#方式二：直接使用装饰器
def api_response(data=None, success=True, message='', code=200, error=None):
    """统一API响应格式"""
    if success:
        response = {
            'success': success,
            'code': code,
            'message': message,
            'data': data,
            'timestamp': int(datetime.now().timestamp())
        }
    else:
        response = {
            "code": code,
            "message": message,
            "error": error,
            "timestamp": int(datetime.now().timestamp())
        }
    return jsonify(response), code

def unified_response(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        # 如果视图返回的是元组，可能已经是 (response, status) 形式
        if isinstance(result, tuple):
            data, code = result[0], result[1] if len(result) >= 2 else 200
        else:
            data, code = result, 200
        #传入的是一个jsonify的对象的化会报错，是一个Response对象，里面有很多属性，请求什么的都在李米娜
        #这里只需要用到json属性即可
        if code == 200:
            return api_response(data=data.json, success=True, code=code,message=data.json.get('message'))
        else:
            return api_response(success=False, message="data not found", code=code, error=data.json.get('error'))
    return wrapper
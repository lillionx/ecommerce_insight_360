"""
E-Commerce Insight 360 - 应用启动入口
项目: 电商全链路数据洞察平台
"""

import os
from app import create_app

# 获取运行环境
env = os.environ.get('FLASK_ENV', 'development')

# 创建Flask应用
app = create_app(env)
app.json.ensure_ascii = False  # 支持中文JSON

@app.route('/')
def index():
    """首页路由"""
    from flask import render_template, jsonify
    from datetime import datetime

    # 返回简单的API信息
    return jsonify({
        'name': 'E-Commerce Insight 360',
        'version': '1.0.0',
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'endpoints': {
            'sales': '/api/stats/sales',
            'funnel': '/api/stats/funnel',
            'products': '/api/stats/products',
            'users': '/api/stats/users',
            'health': '/api/admin/health'
        }
    })


@app.route('/dashboard')
def dashboard():
    """Dashboard页面"""
    from flask import render_template
    return render_template('index.html')


if __name__ == '__main__':
    # 开发环境直接运行
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

"""
E-Commerce Insight 360 - Gunicorn配置文件
项目: 电商全链路数据洞察平台
"""

import multiprocessing
import os

# 服务器socket配置
bind = "0.0.0.0:5000"
backlog = 2048

# Worker进程配置
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# 日志配置
accesslog = "logs/access.log"
errorlog = "logs/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 进程命名
proc_name = "ecommerce_insight_360"

# 服务器机制
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# 预加载应用代码
preload_app = True

# 钩子函数
def on_starting(server):
    """服务器启动时调用"""
    print("E-Commerce Insight 360 正在启动...")


def on_reload(server):
    """服务器重载时调用"""
    print("E-Commerce Insight 360 正在重载...")


def when_ready(server):
    """服务器就绪时调用"""
    print(f"E-Commerce Insight 360 已启动，监听端口: {bind}")


def on_exit(server):
    """服务器退出时调用"""
    print("E-Commerce Insight 360 正在关闭...")

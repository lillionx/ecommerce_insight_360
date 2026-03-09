#!/bin/bash
PID_FILE="/var/run/ecommerce_insight_360.pid"  # 如果有 PID 文件
if [ -f "$PID_FILE" ]; then
    kill -TERM $(cat "$PID_FILE") && rm -f "$PID_FILE"
else
    pkill -f "gunicorn.*run:app"
fi
echo "服务已停止"

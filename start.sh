#!/bin/bash
# 启动电商全链路数据洞察平台服务

set -e  # 遇到错误立即退出

PROJECT_DIR="/opt/ecommerce_insight_360"
CONDA_ENV="eco360"
GUNICORN_CONFIG="gunicorn.conf.py"
APP_MODULE="run:app"
PORT=5000

# 进入项目目录
cd "$PROJECT_DIR" || { echo "错误：项目目录 $PROJECT_DIR 不存在"; exit 1; }

# 1. 激活 Conda 环境（复用部署脚本中的 conda 查找逻辑）
echo "激活 Conda 环境 $CONDA_ENV ..."
if [ -f "/opt/miniconda3/etc/profile.d/conda.sh" ]; then
    source "/opt/miniconda3/etc/profile.d/conda.sh"
elif [ -f "$HOME/miniconda3/etc/profile.d/conda.sh" ]; then
    source "$HOME/miniconda3/etc/profile.d/conda.sh"
else
    echo "错误：未找到 conda 初始化脚本"
    exit 1
fi

# 激活环境（如果环境不存在则报错）
if conda env list | grep -q "^$CONDA_ENV "; then
    conda activate "$CONDA_ENV"
else
    echo "错误：Conda 环境 $CONDA_ENV 不存在"
    exit 1
fi

# 2. 加载环境变量
read -p "请输入数据库用户名" db_user
read -sp "请输入密码" password
export MYSQL_HOST=${MYSQL_HOST:-localhost}
export MYSQL_PORT=${MYSQL_PORT:-3306}
export MYSQL_USER=${MYSQL_USER:-$db_user}
export MYSQL_PASSWORD=${MYSQL_PASSWORD:-$password}
export MYSQL_DATABASE=${MYSQL_DATABASE:-ecommerce_insight}
export FLASK_ENV=${FLASK_ENV:-prroduction}

# 3. 检查端口占用
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "警告：端口 $PORT 已被占用，尝试关闭已有进程..."
    kill -TERM $(lsof -t -i:$PORT) 2>/dev/null || true
    sleep 2
fi

# 4. 启动 Gunicorn（守护进程模式）
echo "启动 Flask 服务..."
gunicorn -c "$GUNICORN_CONFIG" "$APP_MODULE" --daemon

# 5. 等待并验证服务
sleep 3
if curl -s http://localhost:$PORT/api/admin/health > /dev/null 2>&1; then
    echo "服务启动成功！"
    IP=$(hostname -I | awk '{print $1}')
    echo "访问地址: http://$IP:$PORT"
else
    echo "警告：服务启动验证失败，请检查日志"
    echo "日志目录: $PROJECT_DIR/logs/"
fi

#!/bin/bash

#===============================================================================
# E-Commerce Insight 360 一键部署脚本
# 项目: 电商全链路数据洞察平台
# 日期: 2026-03-03
#===============================================================================

set -e  # 遇到错误立即退出

echo "=========================================="
echo "  电商全链路数据洞察平台 - 一键部署"
echo "=========================================="

# 1. 检查并安装Miniconda
echo "[0/7] 检查Miniconda安装..."

# 尝试加载已有的conda初始化脚本
for conda_prefix in "/opt/miniconda3" "$HOME/miniconda3"; do
    if [ -f "$conda_prefix/etc/profile.d/conda.sh" ]; then
        source "$conda_prefix/etc/profile.d/conda.sh"
        break
    fi
done

# 如果conda命令仍不存在，尝试手动加入PATH
if ! command -v conda &> /dev/null; then
    for conda_bin in "/opt/miniconda3/bin/conda" "$HOME/miniconda3/bin/conda"; do
        if [ -x "$conda_bin" ]; then
            export PATH="$(dirname "$conda_bin"):$PATH"
            conda_prefix="$(dirname "$(dirname "$conda_bin")")"
            if [ -f "$conda_prefix/etc/profile.d/conda.sh" ]; then
                source "$conda_prefix/etc/profile.d/conda.sh"
            fi
            break
        fi
    done
fi

# 最终判断
if command -v conda &> /dev/null; then
    echo "  Miniconda已安装: $(conda --version)"
else
    echo "  Miniconda未安装，开始安装..."
    CONDA_INSTALL_PATH="/opt/miniconda3"
    if [ ! -w "$(dirname "$CONDA_INSTALL_PATH")" ]; then
        CONDA_INSTALL_PATH="$HOME/miniconda3"
        echo "  没有权限写入/opt，将安装到 $CONDA_INSTALL_PATH"
    fi
    # 下载安装脚本
    INSTALLER_URL="https://repo.anaconda.com/miniconda/Miniconda3-py311_23.10.0-1-Linux-x86_64.sh"
    INSTALLER_PATH="/tmp/Miniconda3-py311_23.10.0-1-Linux-x86_64.sh"
    if [ ! -f "$INSTALLER_PATH" ]; then
        echo "  下载安装脚本..."
        if command -v wget &> /dev/null; then
            wget -q "$INSTALLER_URL" -O "$INSTALLER_PATH"
        elif command -v curl &> /dev/null; then
            curl -sL "$INSTALLER_URL" -o "$INSTALLER_PATH"
        else
            echo "错误: 需要wget或curl来下载安装脚本"
            exit 1
        fi
    fi
    # 执行静默安装
    echo "  安装Miniconda到 $CONDA_INSTALL_PATH ..."
    bash "$INSTALLER_PATH" -b -u -p "$CONDA_INSTALL_PATH"
    # 将conda的bin加入PATH
    export PATH="$CONDA_INSTALL_PATH/bin:$PATH"
    # 验证安装
    if command -v conda &> /dev/null; then
    export PATH="$CONDA_INSTALL_PATH/bin:$PATH"
    source "$CONDA_INSTALL_PATH/etc/profile.d/conda.sh" 2>/dev/null || true
    # 自动初始化conda，使永久生效
    conda init
    echo "  Miniconda安装成功: $(conda --version)"
    else
        echo "错误: Miniconda安装失败"
        exit 1
    fi
    # 可选：初始化conda（但静默安装已经处理，或者可以运行conda init）
    # 为了后续可以使用conda activate，可以source conda.sh，但脚本中可能不需要
    # source "$CONDA_INSTALL_PATH/etc/profile.d/conda.sh"
fi
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
#创建conda环境
# 2. 添加清华源（仅添加不存在的源）
echo "配置conda源..."

# 定义要添加的源列表（按优先级顺序，越靠前优先级越高）
tsinghua_channels=(
    "https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/"
    "https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/"
    "https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/"
    "https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/"
    "https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/"
    "https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/menpo/"
    "https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/"
)

# 获取当前已配置的channel列表（去掉yaml格式的前导'- '）
current_channels=$(conda config --show channels | grep -E '^\s*-' | sed 's/^\s*-\s*//')

for channel in "${tsinghua_channels[@]}"; do
    if echo "$current_channels" | grep -Fxq "$channel"; then
        :
    else
        echo "  添加源: $channel"
        conda config --add channels "$channel"
    fi
done
echo "[1/7] 创建conda环境"
if conda env list | grep -q "^eco360\s"; then
    echo "环境 eco360 已存在，正在激活..."
    conda activate eco360
else
    echo "环境 eco360 不存在，正在创建..."
    conda create -n eco360 python=3.11 pandas=3.0.1 numpy=1.26.2 flask=2.3.3 "sqlalchemy>=2.0.36" pymysql jinja2 gunicorn python-dotenv python-dateutil pytz pyarrow -y
    conda activate eco360
    pip install werkzeug==3.1.6
    pip install flask-sqlalchemy==3.1.1
    pip install cryptography
echo "  环境配置完成"
fi

# 3. 检查环境
echo "[2/7] 检查部署环境..."

# 检查Python3
if ! command -v python3 &> /dev/null; then
    echo "错误: Python3 未安装"
    exit 1
fi
echo "  Python3: $(python3 --version)"

# 检查pip
if ! command -v pip3 &> /dev/null; then
    echo "错误: pip3 未安装"
    exit 1
fi
echo "  pip3: $(pip3 --version)"

# 检查MySQL客户端
if ! command -v mysql &> /dev/null; then
    echo "警告: MySQL客户端未安装，将跳过数据库检查"
fi

# 4. 创建项目目录
echo "[3/7] 创建项目目录..."
PROJECT_DIR="/opt/ecommerce_insight_360"
mkdir -p $PROJECT_DIR/logs

# 复制项目文件
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cp -r $SCRIPT_DIR/* $PROJECT_DIR/
cd $PROJECT_DIR

echo "  项目目录: $PROJECT_DIR"

# 5. 配置环境变量
read -p "请输入数据库用户名" db_user
read -sp "请输入密码" password
echo "[4/7] 配置环境变量..."
export MYSQL_HOST=${MYSQL_HOST:-localhost}
export MYSQL_PORT=${MYSQL_PORT:-3306}
export MYSQL_USER=${MYSQL_USER:-$db_user}
export MYSQL_PASSWORD=${MYSQL_PASSWORD:-$password}
export MYSQL_DATABASE=${MYSQL_DATABASE:-ecommerce_insight}
export FLASK_ENV=${FLASK_ENV:-prroduction}
echo "  MySQL地址: $MYSQL_HOST:$MYSQL_PORT"
echo "  数据库名: $MYSQL_DATABASE"
# 检查数据库是否存在
if mysql -u "$db_user" -p"$password" -e "USE ecommerce_insight" 2>/dev/null; then
    echo "数据库 ecommerce_insight 已存在，跳过创建"
else
    mysql -u "$db_user" -p"$password" -e "CREATE DATABASE ecommerce_insight CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    echo "数据库 ecommerce_insight 创建成功"
fi

# 6. 初始化数据库
echo "[5/7] 初始化数据库..."
python3 init_database.py
echo "  数据库初始化完成"

# 7. 执行ETL数据导入
echo "[6/7] 执行数据导入..."
python3 -c "
import sys
sys.path.insert(0, '$PROJECT_DIR')
from app.services import etl_service
from datetime import datetime, timedelta
data_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
result = etl_service.run_etl_pipeline(data_date)
print(f'  ETL执行结果: {result[\"status\"]}')
"
echo "  数据导入完成"

# 8. 启动服务
echo "[7/7] 启动Flask服务..."

# 检查端口是否被占用
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "  警告: 端口5000已被占用，尝试关闭已有进程..."
    kill $(lsof -t -i:5000) 2>/dev/null || true
    sleep 2
fi

# 启动gunicorn
gunicorn -c gunicorn.conf.py run:app --daemon

# 等待服务启动
sleep 3

# 验证服务启动
if curl -s http://localhost:5000/api/admin/health > /dev/null 2>&1; then
    echo ""
    echo "=========================================="
    echo "  部署成功！"
    echo "=========================================="
    echo "  访问地址: http://$(hostname -I | awk '{print $1}'):5000"
    echo "  Dashboard: http://$(hostname -I | awk '{print $1}'):5000/dashboard"
    echo "  健康检查: http://$(hostname -I | awk '{print $1}'):5000/api/admin/health"
    echo "=========================================="
else
    echo "警告: 服务启动验证失败，请检查日志"
    echo "日志路径: $PROJECT_DIR/logs/"
fi
#开启防火墙
sudo firewall-cmd --zone=public --add-port=5000/tcp --permanent
sudo firewall-cmd --reload
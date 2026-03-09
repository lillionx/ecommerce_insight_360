/**
 * E-Commerce Insight 360 - Dashboard JavaScript
 */

const API_BASE = '';

// 获取当前日期
function getCurrentDate() {
    const today = new Date();
    return today.toISOString().split('T')[0];
}

// 格式化数字
function formatNumber(num) {
    if (num >= 10000) {
        return (num / 10000).toFixed(1) + '万';
    }
    return num.toLocaleString();
}

// 格式化金额
function formatMoney(amount) {
    return '¥' + parseFloat(amount).toLocaleString('zh-CN', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    });
}


/*
// 初始化销售大盘
async function initSalesDashboard() {
    const date = document.getElementById('datePicker').value || getCurrentDate();

    try {
        // 获取销售汇总数据
        const response = await fetch(`${API_BASE}/api/stats/sales?start_date=${date}&end_date=${date}`);
        const result = await response.json();

        if (result.code === 200 && result.data) {
            const data = result.data;

            // 更新关键指标
            document.getElementById('gmvValue').textContent = formatMoney(data.gmv);
            document.getElementById('ordersValue').textContent = formatNumber(data.total_orders);
            document.getElementById('paidOrdersValue').textContent = formatNumber(data.paid_orders);
            document.getElementById('unitPriceValue').textContent = formatMoney(data.unit_price);

            // 获取趋势数据
            await initSalesTrend(date);
        }
    } catch (error) {
        console.error('Error loading sales data:', error);
    }
}

// 初始化销售趋势图
async function initSalesTrend(date) {
    try {
        const response = await fetch(`${API_BASE}/api/stats/sales/trend?start_date=${date}&end_date=${date}`);
        const result = await response.json();

        if (result.code === 200 && result.data && result.data.trend) {
            const trend = result.data.trend;

            // 更新趋势图
            const trendChart = echarts.init(document.getElementById('trendChart'));
            trendChart.setOption({
                tooltip: {
                    trigger: 'axis'
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: trend.map(item => item.date),
                    axisLine: { lineStyle: { color: '#30363d' } },
                    axisLabel: { color: '#8b949e' }
                },
                yAxis: {
                    type: 'value',
                    lineStyle: { color: '#303 axisLine: {63d}' } ,
                    axisLabel: { color: '#8b949e' },
                    splitLine: { lineStyle: { color: '#21262d' } }
                },
                series: [{
                    name: 'GMV',
                    type: 'line',
                    smooth: true,
                    data: trend.map(item => item.gmv),
                    lineStyle: { color: '#1890ff' },
                    areaStyle: {
                        color: {
                            type: 'linear',
                            x: 0, y: 0, x2: 0, y2: 1,
                            colorStops: [
                                { offset: 0, color: 'rgba(24, 144, 255, 0.3)' },
                                { offset: 1, color: 'rgba(24, 144, 255, 0.05)' }
                            ]
                        }
                    }
                }]
            });
        }
    } catch (error) {
        console.error('Error loading trend data:', error);
    }
}

// 初始化用户漏斗
async function initFunnelChart() {
    const date = document.getElementById('datePicker').value || getCurrentDate();

    try {
        const response = await fetch(`${API_BASE}/api/stats/funnel?date=${date}`);
        const result = await response.json();

        if (result.code === 200 && result.data && result.data.funnel) {
            const funnel = result.data.funnel;

            const funnelChart = echarts.init(document.getElementById('funnelChart'));
            funnelChart.setOption({
                tooltip: {
                    trigger: 'item',
                    formatter: '{b}: {c} ({d}%)'
                },
                series: [{
                    name: '用户漏斗',
                    type: 'funnel',
                    left: '10%',
                    top: 20,
                    bottom: 20,
                    width: '80%',
                    min: 0,
                    max: 100,
                    minSize: '0%',
                    maxSize: '100%',
                    sort: 'descending',
                    gap: 2,
                    label: {
                        show: true,
                        position: 'inside',
                        formatter: '{b}: {c}',
                        color: '#fff'
                    },
                    labelLine: { show: false },
                    itemStyle: { borderColor: '#161b22', borderWidth: 2 },
                    data: funnel.map((item, index) => ({
                        value: item.count,
                        name: item.stage,
                        itemStyle: {
                            color: ['#1890ff', '#52c41a', '#faad14', '#f5222d'][index]
                        }
                    }))
                }]
            });
        }
    } catch (error) {
        console.error('Error loading funnel data:', error);
    }
}

// 初始化商品排行
async function initProductRank() {
    const date = document.getElementById('datePicker').value || getCurrentDate();

    try {
        const response = await fetch(`${API_BASE}/api/stats/products?date=${date}&rank_by=quantity`);
        const result = await response.json();

        if (result.code === 200 && result.data && result.data.top10) {
            const products = result.data.top10;

            const productChart = echarts.init(document.getElementById('productChart'));
            productChart.setOption({
                tooltip: {
                    trigger: 'axis',
                    axisPointer: { type: 'shadow' }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'value',
                    axisLine: { lineStyle: { color: '#30363d' } },
                    axisLabel: { color: '#8b949e' },
                    splitLine: { lineStyle: { color: '#21262d' } }
                },
                yAxis: {
                    type: 'category',
                    data: products.map(p => p.product_name.substring(0, 10)).reverse(),
                    axisLine: { lineStyle: { color: '#30363d' } },
                    axisLabel: { color: '#8b949e' }
                },
                series: [{
                    name: '销量',
                    type: 'bar',
                    data: products.map(p => p.sales_quantity).reverse(),
                    itemStyle: {
                        color: {
                            type: 'linear',
                            x: 0, y: 0, x2: 1, y2: 0,
                            colorStops: [
                                { offset: 0, color: '#1890ff' },
                                { offset: 1, color: '#52c41a' }
                            ]
                        }
                    }
                }]
            });
        }
    } catch (error) {
        console.error('Error loading product data:', error);
    }
}

// 初始化用户分析
async function initUserAnalysis() {
    const date = document.getElementById('datePicker').value || getCurrentDate();

    try {
        const response = await fetch(`${API_BASE}/api/stats/users?date=${date}`);
        const result = await response.json();

        if (result.code === 200 && result.data) {
            // RFM分布
            if (result.data.rfm_distribution) {
                const rfmData = result.data.rfm_distribution;
                const rfmChart = echarts.init(document.getElementById('rfmChart'));
                rfmChart.setOption({
                    tooltip: {
                        trigger: 'item',
                        formatter: '{b}: {c} ({d}%)'
                    },
                    series: [{
                        name: '用户分层',
                        type: 'pie',
                        radius: ['40%', '70%'],
                        avoidLabelOverlap: false,
                        label: {
                            show: true,
                            color: '#fff'
                        },
                        data: rfmData.map((item, index) => ({
                            value: item.count,
                            name: item.level,
                            itemStyle: {
                                color: ['#f5222d', '#faad14', '#52c41a', '#1890ff', '#722ed1'][index]
                            }
                        }))
                    }]
                });
            }

            // 性别分布
            if (result.data.gender_distribution) {
                const genderData = result.data.gender_distribution;
                const genderChart = echarts.init(document.getElementById('genderChart'));
                genderChart.setOption({
                    tooltip: {
                        trigger: 'item',
                        formatter: '{b}: {c} ({d}%)'
                    },
                    series: [{
                        name: '性别分布',
                        type: 'pie',
                        radius: '50%',
                        data: genderData.map(item => ({
                            value: item.count,
                            name: item.gender
                        })),
                        itemStyle: {
                            color: ['#1890ff', '#f5222d', '#8b949e']
                        },
                        label: {
                            show: true,
                            color: '#fff'
                        }
                    }]
                });
            }
        }
    } catch (error) {
        console.error('Error loading user data:', error);
    }
}

// 刷新所有数据
async function refreshAllData() {
    await Promise.all([
        initSalesDashboard(),
        initFunnelChart(),
        initProductRank(),
        initUserAnalysis()
    ]);
}


// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    // 设置日期选择器默认值
    document.getElementById('datePicker').value = getCurrentDate();

    // 绑定日期选择器事件
    document.getElementById('datePicker').addEventListener('change', refreshAllData);

    // 初始化所有图表
    refreshAllData();

    // 窗口大小变化时重新调整图表
    window.addEventListener('resize', function() {
        echarts.getInstanceByDom(document.getElementById('trendChart'))?.resize();
        echarts.getInstanceByDom(document.getElementById('funnelChart'))?.resize();
        echarts.getInstanceByDom(document.getElementById('productChart'))?.resize();
        echarts.getInstanceByDom(document.getElementById('rfmChart'))?.resize();
        echarts.getInstanceByDom(document.getElementById('genderChart'))?.resize();
    });


});
*/

// 总览面板刷新函数
function refreshOverviewPanel() {
    const date = document.getElementById('datePicker').value || getCurrentDate();

    // 获取汇总数据并更新卡片
    fetch(`${API_BASE}/api/stats/sales?start_date=${date}&end_date=${date}`)
        .then(res => res.json())
        .then(result => {
            if (result.code === 200 && result.data) {
                document.getElementById('gmvValue').textContent = formatMoney(result.data.gmv);
                document.getElementById('ordersValue').textContent = formatNumber(result.data.total_orders);
                document.getElementById('paidOrdersValue').textContent = formatNumber(result.data.paid_orders);
                document.getElementById('unitPriceValue').textContent = formatMoney(result.data.unit_price);
            }
        });

    // 获取趋势图数据（使用 trendChart）
    fetch(`${API_BASE}/api/stats/sales/trend?start_date=${'2026-2-2'}&end_date=${date}`)
        .then(res => res.json())
        .then(result => {
            if (result.code === 200 && result.data && result.data.trend) {
                const trend = result.data.trend;
                const chart = echarts.init(document.getElementById('trendChart'));
                chart.setOption({
                tooltip: {
                    trigger: 'axis'
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: trend.map(item => item.date),
                    axisLine: { lineStyle: { color: '#30363d' } },
                    axisLabel: { color: '#8b949e' }
                },
                yAxis: {
                    type: 'value',
                    lineStyle: { color: '#303 axisLine: {63d}' } ,
                    axisLabel: { color: '#8b949e' },
                    splitLine: { lineStyle: { color: '#21262d' } }
                },
                series: [{
                    name: 'GMV',
                    type: 'line',
                    smooth: true,
                    data: trend.map(item => item.gmv),
                    lineStyle: { color: '#1890ff' },
                    areaStyle: {
                        color: {
                            type: 'linear',
                            x: 0, y: 0, x2: 0, y2: 1,
                            colorStops: [
                                { offset: 0, color: 'rgba(24, 144, 255, 0.3)' },
                                { offset: 1, color: 'rgba(24, 144, 255, 0.05)' }
                            ]
                        }
                    }
                }]
            });
            }
        });

    // 漏斗图（funnelChart）
    fetch(`${API_BASE}/api/stats/funnel?start_date=${date}`)
        .then(res => res.json())
        .then(result => {
            if (result.code === 200 && result.data && result.data.funnel) {
                const funnel = result.data.funnel;
                const chart = echarts.init(document.getElementById('funnelChart'));
                chart.setOption({
                tooltip: {
                    trigger: 'item',
                    formatter: '{b}: {c} ({d}%)'
                },
                series: [{
                    name: '用户漏斗',
                    type: 'funnel',
                    left: '10%',
                    top: 20,
                    bottom: 20,
                    width: '80%',
                    min: 0,
                    max: 100,
                    minSize: '0%',
                    maxSize: '100%',
                    sort: 'descending',
                    gap: 2,
                    label: {
                        show: true,
                        position: 'inside',
                        formatter: '{b}: {c}',
                        color: '#fff'
                    },
                    labelLine: { show: false },
                    itemStyle: { borderColor: '#161b22', borderWidth: 2 },
                    data: funnel.map((item, index) => ({
                        value: item.count,
                        name: item.stage,
                        itemStyle: {
                            color: ['#1890ff', '#52c41a', '#faad14', '#f5222d'][index]
                        }
                    }))
                }]
            });
            }
        });

    // 商品排行（productChart）
    fetch(`${API_BASE}/api/stats/products?start_date=${date}&rank_by=quantity`)
        .then(res => res.json())
        .then(result => {
            if (result.code === 200 && result.data && result.data.top10) {
                const products = result.data.top10;
                const chart = echarts.init(document.getElementById('productChart'));
                chart.setOption({
                tooltip: {
                    trigger: 'axis',
                    axisPointer: { type: 'shadow' }
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'value',
                    axisLine: { lineStyle: { color: '#30363d' } },
                    axisLabel: { color: '#8b949e' },
                    splitLine: { lineStyle: { color: '#21262d' } }
                },
                yAxis: {
                    type: 'category',
                    data: products.map(p => p.product_name.substring(0, 10)).reverse(),
                    axisLine: { lineStyle: { color: '#30363d' } },
                    axisLabel: { color: '#8b949e' }
                },
                series: [{
                    name: '销量',
                    type: 'bar',
                    data: products.map(p => p.sales_quantity).reverse(),
                    itemStyle: {
                        color: {
                            type: 'linear',
                            x: 0, y: 0, x2: 1, y2: 0,
                            colorStops: [
                                { offset: 0, color: '#1890ff' },
                                { offset: 1, color: '#52c41a' }
                            ]
                        }
                    }
                }]
            });
            }
        });

    // RFM 和性别分布（rfmChart, genderChart）
    fetch(`${API_BASE}/api/stats/users?date=${date}`)
        .then(res => res.json())
        .then(result => {
            if (result.code === 200 && result.data) {
                if (result.data.rfm_distribution) {
                    const rfmData = result.data.rfm_distribution;
                    const chart = echarts.init(document.getElementById('rfmChart'));
                    chart.setOption({
                    tooltip: {
                        trigger: 'item',
                        formatter: '{b}: {c} ({d}%)'
                    },
                    series: [{
                        name: '用户分层',
                        type: 'pie',
                        radius: ['40%', '70%'],
                        avoidLabelOverlap: false,
                        label: {
                            show: true,
                            color: '#fff'
                        },
                        data: rfmData.map((item, index) => ({
                            value: item.count,
                            name: item.level,
                            itemStyle: {
                                color: ['#f5222d', '#faad14', '#52c41a', '#1890ff', '#722ed1'][index]
                            }
                        }))
                    }]
                });
                }
                if (result.data.gender_distribution) {
                    const genderData = result.data.gender_distribution;
                    const colorMap = {
                                        '男性': '#1890ff',      // 蓝色
                                        '女性': '#f5222d',      // 红色
                                        '未知': '#8b949e'     // 灰色
                                        // 可根据实际返回的性别值添加更多映射
                                    };
                    const chart = echarts.init(document.getElementById('genderChart'));
                    chart.setOption({
                    tooltip: {
                        trigger: 'item',
                        formatter: '{b}: {c} ({d}%)'
                    },
                    series: [{
                        name: '性别分布',
                        type: 'pie',
                        radius: '50%',
                        data: genderData.map(item => ({
                            value: item.count,
                            name: item.gender,
                            itemStyle: {
                                color: colorMap[item.gender] || '#8b949e'   // 若未匹配则使用默认灰色
                            }
                        })),
                        label: {
                            show: true,
                            color: '#fff'
                        }
                    }]
                });
                }
            }
        });


}


// 销售大盘面板刷新
function refreshSalesPanel() {
    const end_date = document.getElementById('datePicker').value || getCurrentDate();
    const start_date = document.getElementById('start_date').value; // 可选月份过滤

    fetch(`${API_BASE}/api/stats/sales/trend?start_date=${start_date}&end_date=${end_date}`)
        .then(res => res.json())
        .then(result => {
            if (result.code === 200 && result.data && result.data.trend) {
                const trend = result.data.trend;
                const chart = echarts.init(document.getElementById('salesTrendChart'));
                chart.setOption({
                tooltip: {
                    trigger: 'axis'
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: trend.map(item => item.date),
                    axisLine: { lineStyle: { color: '#30363d' } },
                    axisLabel: { color: '#8b949e' }
                },
                yAxis: {
                    type: 'value',
                    lineStyle: { color: '#303 axisLine: {63d}' } ,
                    axisLabel: { color: '#8b949e' },
                    splitLine: { lineStyle: { color: '#21262d' } }
                },
                series: [{
                    name: 'GMV',
                    type: 'line',
                    smooth: true,
                    data: trend.map(item => item.gmv),
                    lineStyle: { color: '#1890ff' },
                    areaStyle: {
                        color: {
                            type: 'linear',
                            x: 0, y: 0, x2: 0, y2: 1,
                            colorStops: [
                                { offset: 0, color: 'rgba(24, 144, 255, 0.3)' },
                                { offset: 1, color: 'rgba(24, 144, 255, 0.05)' }
                            ]
                        }
                    }
                }]
            });
            }
        });
    fetch(`${API_BASE}/api/stats/sales/hourly?date=${end_date}`)
        .then(res => res.json())
        .then(result => {
            if (result.code === 200 && result.data && result.data.hourly) {
                const trend = result.data.hourly;
                const chart = echarts.init(document.getElementById('hoursSalesTrendChart'));
                chart.setOption({
                tooltip: {
                    trigger: 'axis'
                },
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                xAxis: {
                    type: 'category',
                    data: trend.map(item => item.hour),
                    axisLine: { lineStyle: { color: '#30363d' } },
                    axisLabel: { color: '#8b949e' }
                },
                yAxis: {
                    type: 'value',
                    lineStyle: { color: '#303 axisLine: {63d}' } ,
                    axisLabel: { color: '#8b949e' },
                    splitLine: { lineStyle: { color: '#21262d' } }
                },
                series: [{
                    name: 'GMV',
                    type: 'line',
                    smooth: true,
                    data: trend.map(item => item.gmv),
                    lineStyle: { color: '#1890ff' },
                    areaStyle: {
                        color: {
                            type: 'linear',
                            x: 0, y: 0, x2: 0, y2: 1,
                            colorStops: [
                                { offset: 0, color: 'rgba(24, 144, 255, 0.3)' },
                                { offset: 1, color: 'rgba(24, 144, 255, 0.05)' }
                            ]
                        }
                    }
                }]
            });
            }
        });
}

// 用户分析面板刷新
function refreshUserPanel() {
    const range = document.getElementById('user-range').value;

    let distUrl, funnelUrl;

    if (range === 'daily') {
        const date = document.getElementById('datePicker').value || getCurrentDate();
        distUrl = `${API_BASE}/api/stats/users/daily?date=${date}`;
        funnelUrl = `${API_BASE}/api/stats/funnel?start_date=${date}`;
    } else {
        const startDate = document.getElementById('overall-start-date').value;
        const endDate = document.getElementById('overall-end-date').value;
        if (!startDate || !endDate) {
            alert('请选择开始和结束日期');
            return;
        }
        distUrl = `${API_BASE}/api/stats/users/period?start_date=${startDate}&end_date=${endDate}`;
        funnelUrl = `${API_BASE}/api/stats/funnel?start_date=${startDate}&end_date=${endDate}`;
    }

    Promise.all([
        fetch(distUrl).then(res => res.json()),
        fetch(funnelUrl).then(res => res.json())
    ])
    .then(([distResult, funnelResult]) => {
        if (distResult.code === 200 && distResult.data) {
            renderUserDistCharts(distResult.data);
        } else {
            console.error('分布数据加载失败:', distResult.message);
        }
        if (funnelResult.code === 200 && funnelResult.data && funnelResult.data.funnel) {
            renderFunnelChart('userFunnelChart', funnelResult.data.funnel);
        } else {
            console.error('漏斗数据加载失败:', funnelResult.message);
        }
    })
    .catch(err => console.error('用户数据请求失败:', err));
}


// 渲染漏斗图（优化宽度，避免过宽）
function renderFunnelChart(containerId, funnelData) {
    const chart = echarts.init(document.getElementById(containerId));
    chart.setOption({
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)'
        },
        series: [{
            name: '用户漏斗',
            type: 'funnel',
            left: '40%',          // 增加左留白
            right: '40%',          // 增加右留白，使漏斗变窄
            top: 30,               // 适当增加上下留白
            bottom: 30,
            // width 由 left/right 自动决定，无需设置
            min: 0,
            max: Math.max(...funnelData.map(item => item.count)),
            minSize: '0%',
            maxSize: '100%',
            sort: 'descending',
            gap: 2,
            label: {
                show: true,
                position: 'inside', // 也可改为 'right' 或 'left' 避免标签挤压
                formatter: '{b}: {c}',
                color: '#fff'
            },
            labelLine: { show: false },
            itemStyle: { borderColor: '#161b22', borderWidth: 2 },
            data: funnelData.map((item, index) => ({
                value: item.count,
                name: item.stage,
                itemStyle: {
                    color: ['#1890ff', '#52c41a', '#faad14', '#f5222d'][index % 4]
                }
            }))
        }]
    });
}

// 渲染四个图表
function renderUserDistCharts(data) {
    // 1. RFM 分层（饼图）
    if (data.rfm_distribution) {
        const rfmChart = echarts.init(document.getElementById('userRfmChart'));
        rfmChart.setOption({
            tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
            series: [{
                name: 'RFM分层',
                type: 'pie',
                radius: ['40%', '70%'],
                data: data.rfm_distribution.map(item => ({
                    value: item.count,
                    name: item.level,
                    itemStyle: { color: getLevelColor(item.level) }
                })),
                label: { show: true, color: '#fff' }
            }]
        });
    }

    // 2. 性别分布（饼图）
    if (data.gender_distribution) {
        const genderChart = echarts.init(document.getElementById('userGenderChart'));
        genderChart.setOption({
            tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
            series: [{
                name: '性别分布',
                type: 'pie',
                radius: '50%',
                data: data.gender_distribution.map(item => ({
                    value: item.count,
                    name: item.gender,
                    itemStyle: { color: getGenderColor(item.gender) }
                })),
                label: { show: true, color: '#fff' }
            }]
        });
    }

    // 3. 年龄分布（柱状图或饼图，这里用饼图）
    if (data.age_distribution) {
        const ageChart = echarts.init(document.getElementById('userAgeChart'));
        ageChart.setOption({
            tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
            series: [{
                name: '年龄分布',
                type: 'pie',
                radius: ['40%', '70%'],
                data: data.age_distribution.map(item => ({
                    value: item.count,
                    name: item.age_group || item.age,  // 根据实际字段调整
                    itemStyle: { color: getAgeColor(item.age_group) }
                })),
                label: { show: true, color: '#fff' }
            }]
        });
    }

    // 4. 城市分布（饼图，若城市过多可改用柱状图，这里先用饼图展示前10）
    if (data.city_distribution) {
        const cityChart = echarts.init(document.getElementById('userCityChart'));
        // 限制显示前10个城市，其余归为“其他”
        let cities = data.city_distribution;
        if (cities.length > 10) {
            const top10 = cities.slice(0, 10);
            const others = cities.slice(10).reduce((sum, item) => sum + item.count, 0);
            cities = [...top10, { city: '其他', count: others }];
        }
        cityChart.setOption({
            tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
            series: [{
                name: '城市分布',
                type: 'pie',
                radius: ['40%', '70%'],
                data: cities.map(item => ({
                    value: item.count,
                    name: item.city,
                    itemStyle: { color: getCityColor(item.city) }
                })),
                label: { show: true, color: '#fff' }
            }]
        });
    }
}

// 辅助颜色函数（可根据实际需要扩展）
function getLevelColor(level) {
    const colorMap = {
        'new': '#f5222d',
        'medium_value': '#faad14',
        'low_value': '#52c41a',
        'unknown': '#8b949e'
    };
    return colorMap[level] || '#1890ff';
}

function getGenderColor(gender) {
    const colorMap = {
        '男性': '#1890ff',
        '女性': '#f5222d',
    };
    return colorMap[gender] || '#1890ff';
}

function getAgeColor(ageRange) {
    const colorMap = {
        '18岁以下': '#1890ff',
        "18-24岁": '#52c41a',
        '25-34岁': '#faad14',
        '35-44岁': '#f5222d',
        '45-54以上': '#722ed1',
        '55岁及以上': '#fa541c'
    };
    return colorMap[ageRange] || '#8b949e';
}

function getCityColor(city) {
    // 随机或固定颜色，此处简化处理，可返回一个默认颜色数组
    const colors = ['#1890ff', '#52c41a', '#faad14', '#f5222d', '#722ed1', '#13c2c2', '#eb2f96', '#2f54eb'];
    let hash = 0;
    for (let i = 0; i < city.length; i++) {
        hash = city.charCodeAt(i) + ((hash << 5) - hash);
    }
    return colors[Math.abs(hash) % colors.length];
}



// 商品分析面板刷新
function refreshProductPanel() {
    const range = document.getElementById('product-range').value;
    const sortBy = document.querySelector('input[name="product-sort"]:checked').value;

    let rankUrl, typeUrl;

    if (range === 'daily') {
        const date = document.getElementById('datePicker').value || getCurrentDate();
        rankUrl = `${API_BASE}/api/stats/products?start_date=${date}&rank_by=${sortBy}`;
        typeUrl = `${API_BASE}/api/stats/products/category?start_date=${date}`;
    } else {
        const startDate = document.getElementById('product-start-date').value;
        const endDate = document.getElementById('product-end-date').value;
        if (!startDate || !endDate) {
            alert('请选择开始和结束日期');
            return;
        }
        rankUrl = `${API_BASE}/api/stats/products?start_date=${startDate}&end_date=${endDate}&rank_by=${sortBy}`;
        typeUrl = `${API_BASE}/api/stats/products/category?start_date=${startDate}&end_date=${endDate}`;
    }

    // 并发请求两个图表数据
    Promise.all([
        fetch(rankUrl).then(res => res.json()),
        fetch(typeUrl).then(res => res.json())
    ])
    .then(([rankResult, typeResult]) => {
        // 商品排行图
        if (rankResult.code === 200 && rankResult.data && rankResult.data.top10) {
            renderProductRankChart(rankResult.data.top10, sortBy);
        } else {
            console.error('商品排行数据加载失败:', rankResult.message);
            // 可显示空图表或提示
        }

        // 商品种类占比图
        if (typeResult.code === 200 && typeResult.data && typeResult.data.distribution) {
            renderProductTypeChart(typeResult.data.distribution);
        } else {
            console.error('商品种类数据加载失败:', typeResult.message);
        }
    })
    .catch(err => console.error('商品数据请求失败:', err));

    // 商品信息查看部分保持不变（由按钮触发）
}

function renderProductRankChart(products, sortBy) {
    const chart = echarts.init(document.getElementById('productRankChart'));
    const seriesName = sortBy === 'quantity' ? '销量' : '销售额';
    const dataField = sortBy === 'quantity' ? 'sales_quantity' : 'sales_amount';

    chart.setOption({
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
        xAxis: {
            type: 'value',
            axisLine: { lineStyle: { color: '#30363d' } },
            axisLabel: { color: '#8b949e' },
            splitLine: { lineStyle: { color: '#21262d' } }
        },
        yAxis: {
            type: 'category',
            data: products.map(p => p.product_name.substring(0, 10)).reverse(),
            axisLine: { lineStyle: { color: '#30363d' } },
            axisLabel: { color: '#8b949e' }
        },
        series: [{
            name: seriesName,
            type: 'bar',
            data: products.map(p => p[dataField]).reverse(),
            itemStyle: {
                color: {
                    type: 'linear',
                    x: 0, y: 0, x2: 1, y2: 0,
                    colorStops: [
                        { offset: 0, color: '#1890ff' },
                        { offset: 1, color: '#52c41a' }
                    ]
                }
            }
        }]
    });
}

function renderProductTypeChart(categories) {
    const chart = echarts.init(document.getElementById('productTypeChart'));
    chart.setOption({
        tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
        series: [{
            name: '商品类别占比',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: { show: true, color: '#fff' },
            data: categories.map(item => ({
                value: item.order_count,
                name: item.category,
                itemStyle: { color: getCategoryColor(item.category) } // 使用已有颜色映射
            }))
        }]
    });
}
// 可选：为不同类别分配固定颜色
function getCategoryColor(category) {
    const categoryColorMap = {
    '服装': '#f5222d',    // 红色
    '食品': '#52c41a',    // 绿色
    '家居': '#faad14',    // 橙色/金色
    '图书': '#1890ff',    // 蓝色
    '运动': '#722ed1',    // 紫色
    '美妆': '#eb2f96',    // 粉红
    '玩具': '#13c2c2',    // 青色
    '电子产品': '#2f54eb'  // 深蓝
    };
    return categoryColorMap[category] || '#8b949e';
}


// 刷新订单管理面板
function refreshOrderPanel() {
    const date = document.getElementById('datePicker').value || getCurrentDate();
    const status = document.getElementById('order-status').value; // 获取选中的状态值

    let url = `${API_BASE}/api/stats/products/orders?date=${date}`;
    if (status) {  // 如果状态不为空字符串，则添加到 URL
        url += `&status=${encodeURIComponent(status)}`;
    }

    fetch(url)
        .then(res => res.json())
        .then(result => {
            if (result.code === 200 && result.data) {
                const orders = result.data.result;
                renderOrderTable(orders);
            } else {
                console.error('订单数据加载失败:', result.message);
                document.getElementById('order-table').innerHTML = '<div class="no-data">加载失败</div>';
            }
        })
        .catch(err => {
            console.error('订单请求失败:', err);
            document.getElementById('order-table').innerHTML = '<div class="no-data">请求异常</div>';
        });
}

// 渲染订单表格
function renderOrderTable(orders) {
    const container = document.getElementById('order-table');
    container.innerHTML = ''; // 清空

    if (!orders || orders.length === 0) {
        container.innerHTML = '<div class="no-data">暂无订单</div>';
        return;
    }

    const table = document.createElement('table');
    table.className = 'order-table';

    // 表头
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    ['订单ID', '用户ID', '商品ID', '金额', '数量', '状态', '创建时间', '支付时间'].forEach(text => {
        const th = document.createElement('th');
        th.textContent = text;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // 表体
    const tbody = document.createElement('tbody');
    orders.forEach(order => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${order.order_id}</td>
            <td>${order.user_id}</td>
            <td>${order.product_id}</td>
            <td>${formatMoney(order.amount)}</td>
            <td>${order.quantity}</td>
            <td>${order.status}</td>
            <td>${order.create_time ? order.create_time.slice(0, 19).replace('T', ' ') : '-'}</td>
            <td>${order.pay_time ? order.pay_time.slice(0, 19).replace('T', ' ') : '-'}</td>
        `;
        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    container.appendChild(table);
}
// 显示默认提示
function showProductInfoPlaceholder() {
    const container = document.getElementById('productInfoChart');
    container.innerHTML = '<div class="no-data">请输入商品ID查询</div>';
}

// 根据商品ID查询详情
function fetchProductById(productId) {
    if (!productId) {
        showProductInfoPlaceholder();
        return;
    }

    fetch(`${API_BASE}/api/stats/products/details?product_id=${productId}`)
        .then(res => res.json())
        .then(result => {
            if (result.code === 200 && result.data) {
                renderSingleProduct(result.data);
            } else {
                // 接口返回错误或未找到商品
                const container = document.getElementById('productInfoChart');
                container.innerHTML = '<div class="no-data">未找到该商品</div>';
            }
        })
        .catch(err => {
            console.error('商品详情加载失败:', err);
            const container = document.getElementById('productInfoChart');
            container.innerHTML = '<div class="no-data">查询失败，请稍后重试</div>';
        });
}

// 渲染单个商品表格
function renderSingleProduct(product) {
    const container = document.getElementById('productInfoChart');
    container.innerHTML = ''; // 清空

    const table = document.createElement('table');
    table.className = 'product-info-table';

    // 表头
    const thead = document.createElement('thead');
    const headerRow = document.createElement('tr');
    ['商品ID', '商品名称', '类别', '价格', '库存', '创建时间', '更新时间'].forEach(text => {
        const th = document.createElement('th');
        th.textContent = text;
        headerRow.appendChild(th);
    });
    thead.appendChild(headerRow);
    table.appendChild(thead);

    // 表体（只有一行）
    const tbody = document.createElement('tbody');
    const row = document.createElement('tr');
    row.innerHTML = `
        <td>${product.product_id}</td>
        <td>${product.product_name}</td>
        <td>${product.category}</td>
        <td>${formatMoney(product.price)}</td>
        <td>${product.stock}</td>
        <td>${product.create_time || '-'}</td>
        <td>${product.update_time || '-'}</td>
    `;
    tbody.appendChild(row);
    table.appendChild(tbody);

    container.appendChild(table);
}


// 面板配置映射
const panels = {
    'all_table': refreshOverviewPanel,
    'sales': refreshSalesPanel,
    'user': refreshUserPanel,
    'products_rank': refreshProductPanel,
    'order': refreshOrderPanel   // 新增
};

// 切换面板函数
function switchPanel(panelId) {
    // 隐藏所有面板
    document.querySelectorAll('.content-panel').forEach(p => p.classList.remove('active'));
    // 显示目标面板
    const targetPanel = document.getElementById(`panel-${panelId}`);
    if (targetPanel) targetPanel.classList.add('active');

    // 更新菜单激活状态
    document.querySelectorAll('.sidebar-menu-item').forEach(item => item.classList.remove('active'));
    const menuItem = document.getElementById(panelId);
    if (menuItem) menuItem.classList.add('active');

    // 刷新对应面板数据
    if (panels[panelId]) panels[panelId]();
}

// 绑定菜单点击事件
document.querySelectorAll('.sidebar-menu-item').forEach(item => {
    item.addEventListener('click', function() {
        switchPanel(this.id);
    });
});


// 为销售大盘的月份选择绑定事件
document.getElementById('sales-month')?.addEventListener('change', function() {
    if (document.getElementById('panel-sales').classList.contains('active')) {
        refreshSalesPanel();
    }
});

// 为用户分析的用户类型选择绑定事件
document.getElementById('user-type')?.addEventListener('change', function() {
    if (document.getElementById('panel-user').classList.contains('active')) {
        refreshUserPanel();
    }
});

// 为商品分析的排序单选按钮绑定事件
document.querySelectorAll('input[name="product-sort"]').forEach(radio => {
    radio.addEventListener('change', function() {
        if (document.getElementById('panel-products_rank').classList.contains('active')) {
            refreshProductPanel();
        }
    });
});

// 为订单管理的状态选择绑定事件
document.getElementById('order-status')?.addEventListener('change', function() {
    if (document.getElementById('panel-order').classList.contains('active')) {
        refreshOrderPanel();
    }
});



// 全局日期变化时，刷新当前激活的面板
document.getElementById('datePicker').addEventListener('change', function() {
    const activePanel = document.querySelector('.content-panel.active');
    if (activePanel) {
        const panelId = activePanel.id.replace('panel-', '');
        if (panels[panelId]) panels[panelId]();
    }
});

// 起始日期变化时，刷新当前激活面板
document.getElementById('start_date').addEventListener('change', function() {
    const activePanel = document.querySelector('.content-panel.active');
    if (activePanel) {
        const panelId = activePanel.id.replace('panel-', '');
        if (panels[panelId]) panels[panelId]();
    }
});

// 窗口大小变化时，调整所有已初始化的图表
window.addEventListener('resize', function() {
    // 总览面板图表
    ['trendChart', 'funnelChart', 'productChart', 'rfmChart', 'genderChart'].forEach(id => {
        echarts.getInstanceByDom(document.getElementById(id))?.resize();
    });
    // 销售面板图表
    echarts.getInstanceByDom(document.getElementById('salesTrendChart'))?.resize();
    // 用户面板图表
    ['userFunnelChart', 'userRfmChart', 'userGenderChart'].forEach(id => {
        echarts.getInstanceByDom(document.getElementById(id))?.resize();
    });
    // 商品面板图表
    echarts.getInstanceByDom(document.getElementById('productRankChart'))?.resize();
    // 订单面板无图表，可忽略
});

// 页面加载完成时，初始化默认面板（总览）
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('datePicker').value = getCurrentDate();
    refreshOverviewPanel(); // 初始化总览

    // 商品查询
    const searchBtn = document.getElementById('searchProductBtn');
    const resetBtn = document.getElementById('resetProductBtn');
    const productIdInput = document.getElementById('productIdInput');

    if (searchBtn) {
        searchBtn.addEventListener('click', function() {
            const id = productIdInput.value.trim();
            if (id === '') {
                showProductInfoPlaceholder(); // 输入为空时显示提示
            } else {
                fetchProductById(id);
            }
        });
    }

    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            productIdInput.value = '';          // 清空输入框
            showProductInfoPlaceholder();        // 恢复提示
        });
    }

    // 支持回车查询
    if (productIdInput) {
        productIdInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchBtn.click();
            }
        });
    }


    // 订单状态筛选
    const orderStatus = document.getElementById('order-status');
    if (orderStatus) {
        orderStatus.addEventListener('change', function() {
            // 仅在当前激活面板为订单管理时刷新
            if (document.getElementById('panel-order').classList.contains('active')) {
                refreshOrderPanel();
            }
        });
    }


    // 定义一次 today 和 sevenDaysAgo，供两个面板使用
    const today = new Date();
    const sevenDaysAgo = new Date(today);
    sevenDaysAgo.setDate(today.getDate() - 6); // 最近7天（含今天）




    // ---------- 用户分析面板初始化 ----------
    const userRangeSelect = document.getElementById('user-range');
    const userDateRangePicker = document.getElementById('date-range-picker');
    const userStart = document.getElementById('overall-start-date');
    const userEnd = document.getElementById('overall-end-date');

    if (userStart && userEnd) {
        userStart.value = sevenDaysAgo.toISOString().split('T')[0];
        userEnd.value = today.toISOString().split('T')[0];
    }

    if (userRangeSelect) {
        userRangeSelect.addEventListener('change', function() {
            if (userDateRangePicker) {
                userDateRangePicker.style.display = this.value === 'overall' ? 'flex' : 'none';
            }
            if (document.getElementById('panel-user').classList.contains('active')) {
                refreshUserPanel();
            }
        });
    }

    if (userStart && userEnd) {
        userStart.addEventListener('change', function() {
            if (userRangeSelect && userRangeSelect.value === 'overall' &&
                document.getElementById('panel-user').classList.contains('active')) {
                refreshUserPanel();
            }
        });
        userEnd.addEventListener('change', function() {
            if (userRangeSelect && userRangeSelect.value === 'overall' &&
                document.getElementById('panel-user').classList.contains('active')) {
                refreshUserPanel();
            }
        });
    }

    // 初始隐藏日期范围选择器（如果总体模式不是默认）
    if (userDateRangePicker && userRangeSelect && userRangeSelect.value !== 'overall') {
        userDateRangePicker.style.display = 'none';
    }

    // ---------- 商品分析面板初始化 ----------
    const productRangeSelect = document.getElementById('product-range');
    const productDateRangePicker = document.getElementById('product-date-range-picker');
    const productStart = document.getElementById('product-start-date');
    const productEnd = document.getElementById('product-end-date');

    if (productStart && productEnd) {
        productStart.value = sevenDaysAgo.toISOString().split('T')[0];
        productEnd.value = today.toISOString().split('T')[0];
    }

    if (productRangeSelect) {
        productRangeSelect.addEventListener('change', function() {
            if (productDateRangePicker) {
                productDateRangePicker.style.display = this.value === 'overall' ? 'flex' : 'none';
            }
            if (document.getElementById('panel-products_rank').classList.contains('active')) {
                refreshProductPanel();
            }
        });
    }

    if (productStart && productEnd) {
        productStart.addEventListener('change', function() {
            if (productRangeSelect && productRangeSelect.value === 'overall' &&
                document.getElementById('panel-products_rank').classList.contains('active')) {
                refreshProductPanel();
            }
        });
        productEnd.addEventListener('change', function() {
            if (productRangeSelect && productRangeSelect.value === 'overall' &&
                document.getElementById('panel-products_rank').classList.contains('active')) {
                refreshProductPanel();
            }
        });
    }

    // 初始隐藏商品分析日期范围选择器（如果总体模式不是默认）
    if (productDateRangePicker && productRangeSelect && productRangeSelect.value !== 'overall') {
        productDateRangePicker.style.display = 'none';
    }

});
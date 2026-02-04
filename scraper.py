import requests
from bs4 import BeautifulSoup
import json
import random
from datetime import datetime
import time

# ================= 配置区 =================

# 模拟真实浏览器，防止被当作机器人拦截
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

# 基准数据 (保持不变)
ENTERPRISE_DATA = [
    {"name": "阿里 (Alibaba)", "count": "100,000+", "chips": "H800/A800/平头哥", "trend": "自研占比↑", "isHBM": False},
    {"name": "腾讯 (Tencent)", "count": "90,000+", "chips": "H800/星脉网络", "trend": "混元扩容", "isHBM": True},
    {"name": "字节跳动 (ByteDance)", "count": "150,000+", "chips": "H20/H800/L20", "trend": "极其激进", "isHBM": True},
    {"name": "百度 (Baidu)", "count": "60,000+", "chips": "昆仑芯/昇腾/A800", "trend": "国产替代", "isHBM": False},
    {"name": "华为 (Huawei Cloud)", "count": "Hidden", "chips": "Ascend 910B Cluster", "trend": "产能爬坡", "isHBM": True},
    {"name": "金山云 (Kingsoft)", "count": "15,000+", "chips": "A100/H800", "trend": "小米生态", "isHBM": False},
]

AUTO_DATA = [
    {"name": "Tesla", "count": "100E (Dojo+H100)", "chipType": "HW4.0 / H100 Cluster", "news": "FSD v13 推送准备中"},
    {"name": "华为车BU", "count": "3.5E FLOPS", "chipType": "Ascend 610/910", "news": "ADS 3.0 无图商用"},
    {"name": "小鹏 (Xpeng)", "count": "2.51E FLOPS", "chipType": "扶摇架构/阿里云", "news": "端到端大模型上车"},
    {"name": "理想 (Li Auto)", "count": "2.4E FLOPS", "chipType": "NVIDIA Orin-X 集群", "news": "训练里程破亿"},
    {"name": "小米汽车", "count": "未公开 (高算力)", "chipType": "NVIDIA Orin + 云端", "news": "城市 NOA 快速开通"},
]

# ================= 核心抓取逻辑 =================

def fetch_ithome_tag():
    """
    策略A: 抓取 IT之家 的 'Nvidia' 标签页
    页面结构通常比较稳定
    """
    url = "https://www.ithome.com/tag/nvidia/"
    print(f"正在尝试抓取: {url}")
    news_list = []
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8' # 强制编码
        
        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # IT之家电脑版标签页结构通常是 .block .media-content
        # 我们尝试找新闻列表容器
        items = soup.select('.news-box .list-con li')
        
        # 如果上面的没找到，尝试另一种常见结构
        if not items:
            items = soup.select('.bl')

        print(f"找到 {len(items)} 个潜在条目")

        for item in items[:8]: # 只取前8条
            # 提取链接和标题
            link_tag = item.find('a')
            if not link_tag: continue
            
            title = link_tag.get_text().strip()
            href = link_tag.get('href')
            
            # 过滤掉非新闻的广告或无效条目
            if not title or len(title) < 5: continue
            
            # 提取时间 (通常在 span 标签或者直接写在 li 里)
            date_tag = item.find('span', class_='date') or item.find('i')
            date_str = date_tag.get_text().strip() if date_tag else "近期"
            
            # 处理时间格式，如果是 "1小时前" 这种，保留原样即可，或者获取当前日期
            if "前" in date_str or not date_str:
                date_str = datetime.now().strftime("%m-%d")

            news_list.append({
                "source": "ITHome",
                "date": date_str,
                "title": title,
                "url": href
            })
            
    except Exception as e:
        print(f"ITHome 抓取报错: {e}")
        
    return news_list

def fetch_sina_tech():
    """
    策略B: 抓取新浪科技 5G/AI 频道 (备用源)
    """
    url = "https://finance.sina.com.cn/7x24/" # 7x24小时快讯，非常适合做情报
    print(f"正在尝试抓取: {url}")
    news_list = []
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8' 
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 新浪快讯结构
        items = soup.select('.bd_list .bd_i')
        
        for item in items[:6]:
            text_p = item.find('p', class_='bd_i_txt_c')
            if not text_p: continue
            
            # 快讯通常没有标题，只有一段话，我们截取前30个字做标题
            full_text = text_p.get_text().strip()
            title = full_text[:40] + "..." if len(full_text) > 40 else full_text
            
            # 筛选关键词，只保留相关的
            keywords = ['AI', 'GPU', '芯片', '算力', '英伟达', '华为', 'OpenAI', '半导体']
            if not any(k in full_text for k in keywords):
                continue
                
            time_tag = item.find('span', class_='bd_i_time_c')
            time_str = time_tag.get_text().strip() if time_tag else "今日"

            news_list.append({
                "source": "Sina 7x24",
                "date": time_str,
                "title": title,
                "url": "https://finance.sina.com.cn/7x24/" # 快讯没有独立链接，跳到主页
            })
            
    except Exception as e:
        print(f"Sina 抓取报错: {e}")

    return news_list

def main():
    print("=== 开始执行抓取任务 ===")
    
    # 1. 尝试抓取 IT之家
    news = fetch_ithome_tag()
    
    # 2. 如果 IT之家 数据太少，尝试抓取新浪作为补充
    if len(news) < 3:
        print("IT之家数据不足，启用新浪备用源...")
        sina_news = fetch_sina_tech()
        news.extend(sina_news)
    
    # 3. 如果还是完全没有数据 (极端情况)，插入一条提示新闻
    if not news:
        news.append({
            "source": "System",
            "date": datetime.now().strftime("%H:%M"),
            "title": "当前网络波动，暂未获取到最新源，请稍后重试。",
            "url": "#"
        })
        # 插入一条硬编码的兜底新闻，保证版面不空
        news.append({
            "source": "Market",
            "date": "2024",
            "title": "英伟达 B200 芯片出货预期向好 (历史数据)",
            "url": "https://www.nvidia.com"
        })

    print(f"最终获取新闻条数: {len(news)}")

    # 4. 组装数据
    final_data = {
        "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "enterprise": ENTERPRISE_DATA,
        "auto": AUTO_DATA,
        "news": news
    }
    
    # 5. 写入文件
    try:
        json_str = json.dumps(final_data, ensure_ascii=False, indent=2)
        with open("data.js", "w", encoding="utf-8") as f:
            f.write(f"const gpuData = {json_str};")
        print("✅ data.js 写入成功")
    except Exception as e:
        print(f"❌ 文件写入失败: {e}")

if __name__ == "__main__":
    main()

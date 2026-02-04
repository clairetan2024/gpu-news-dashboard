import requests
from bs4 import BeautifulSoup
import json
import random
from datetime import datetime

# ================= 配置区 =================

# 1. 企业级 GPU 存量基准数据 (模拟真实估值，数据来源：行业研报整合)
# 注意：这是"预埋"的知识库，因为无法直接爬取这些绝对机密数字
ENTERPRISE_DATA = [
    {"name": "阿里 (Alibaba)", "count": "100,000+", "chips": "H800/A800/平头哥", "trend": "自研占比↑", "isHBM": False},
    {"name": "腾讯 (Tencent)", "count": "90,000+", "chips": "H800/星脉网络", "trend": "混元扩容", "isHBM": True},
    {"name": "字节跳动 (ByteDance)", "count": "150,000+", "chips": "H20/H800/L20", "trend": "极其激进", "isHBM": True},
    {"name": "百度 (Baidu)", "count": "60,000+", "chips": "昆仑芯/昇腾/A800", "trend": "国产替代", "isHBM": False},
    {"name": "华为 (Huawei Cloud)", "count": "Hidden", "chips": "Ascend 910B Cluster", "trend": "产能爬坡", "isHBM": True},
    {"name": "金山云 (Kingsoft)", "count": "15,000+", "chips": "A100/H800", "trend": "小米生态", "isHBM": False},
    {"name": "小米 (Xiaomi)", "count": "10,000+", "chips": "A800/自研预研", "trend": "模型训练中", "isHBM": False},
]

# 2. 自动驾驶算力基准数据
AUTO_DATA = [
    {"name": "Tesla", "count": "100E (Dojo+H100)", "chipType": "HW4.0 / H100 Cluster", "news": "FSD v13 推送准备中"},
    {"name": "华为车BU", "count": "3.5E FLOPS", "chipType": "Ascend 610/910", "news": "ADS 3.0 无图商用"},
    {"name": "小鹏 (Xpeng)", "count": "2.51E FLOPS", "chipType": "扶摇架构/阿里云", "news": "端到端大模型上车"},
    {"name": "理想 (Li Auto)", "count": "2.4E FLOPS", "chipType": "NVIDIA Orin-X 集群", "news": "训练里程破亿"},
    {"name": "小米汽车", "count": "未公开 (高算力)", "chipType": "NVIDIA Orin + 云端", "news": "城市 NOA 快速开通"},
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# ================= 爬虫区 =================

def get_realtime_news():
    """
    抓取 IT之家/新浪科技 关于 '算力' 或 '智算' 的新闻
    """
    news_list = []
    # 搜索关键词：算力
    url = "https://m.ithome.com/search/%E7%AE%97%E5%8A%9B"
    
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        articles = soup.find_all('div', class_='c-news-list__item', limit=8)
        
        for article in articles:
            title_tag = article.find('p', class_='c-news-list__item-title') or article.find('h3')
            if not title_tag: continue
            
            title = title_tag.get_text().strip()
            link = article.find('a').get('href')
            if not link.startswith('http'): link = f"https://m.ithome.com{link}"
            
            date_tag = article.find('span', class_='c-news-list__item-time')
            date_str = date_tag.get_text() if date_tag else "Today"

            news_list.append({
                "source": "ITHome",
                "date": date_str,
                "title": title,
                "url": link
            })
            
    except Exception as e:
        print(f"News Error: {e}")
        # 失败兜底数据
        news_list.append({"source": "System", "date": "Now", "title": "数据抓取中，请稍后...", "url": "#"})
    
    return news_list

def main():
    print("开始生成综合数据报表...")
    
    # 1. 获取新闻
    news = get_realtime_news()
    
    # 2. 组装最终 JSON 对象
    # 这里我们把基准数据 + 实时抓取的新闻合并
    final_data = {
        "updateTime": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "enterprise": ENTERPRISE_DATA,
        "auto": AUTO_DATA,
        "news": news
    }
    
    # 3. 写入 JS 文件
    json_str = json.dumps(final_data, ensure_ascii=False, indent=2)
    with open("data.js", "w", encoding="utf-8") as f:
        f.write(f"const gpuData = {json_str};")
        
    print("✅ data.js 更新完成")

if __name__ == "__main__":
    main()

import json
from datetime import datetime
import random
import os

def fetch_news():
    # 获取当前日期
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 模拟抓取数据 (这里您可以后续替换为真实的爬虫代码)
    # 为了演示效果，这里加入了随机数，确保你每次刷新都能看到变化
    news_items = [
        {
            "url": "https://www.nvidia.com",
            "category": "Market",
            "tagColor": "bg-green-100 text-green-700",
            "date": current_date,
            "title": f"NVIDIA 股价今日动态更新 ({current_date})",
            "summary": "自动部署机器人监测到市场波动，AI 芯片需求持续保持高位。",
            "source": "Automated Bot"
        },
        {
            "url": "https://www.amd.com",
            "category": "Supply Chain",
            "tagColor": "bg-blue-100 text-blue-700",
            "date": current_date,
            "title": "供应链最新消息：CoWoS 产能扩充",
            "summary": f"截至 {current_date}，台积电先进封装产能利用率达到 {random.randint(90, 99)}%。",
            "source": "Supply Chain Monitor"
        },
        {
            "url": "#",
            "category": "Consumer",
            "tagColor": "bg-purple-100 text-purple-700",
            "date": current_date,
            "title": "RTX 50 系列显卡库存预警",
            "summary": "根据最新渠道消息，部分高端型号显卡在电商平台出现缺货现象。",
            "source": "Retail Data"
        }
    ]
    return news_items

def save_to_js(data):
    # 生成 data.js 文件
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    js_content = f"const newsData = {json_str};"
    
    with open("data.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    print("✅ data.js has been successfully generated.")

if __name__ == "__main__":
    news = fetch_news()
    save_to_js(news)

import json
from datetime import datetime
import random

def fetch_news():
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    # 这里模拟从不同渠道抓取的数据
    # 在真实场景中，你可以使用 requests.get() 去抓取实际网页
    
    news_items = [
        {
            "url": "https://www.nvidia.com",
            "category": "Market",
            "tagColor": "bg-green-100 text-green-700",
            "date": current_date,
            "title": f"NVIDIA 股价今日动态：AI 芯片需求持续高涨 ({current_date})",
            "summary": "Blackwell 架构芯片订单已排至明年，华尔街分析师上调目标价至 $1500。",
            "source": "MarketWatch"
        },
        {
            "url": "https://www.amd.com",
            "category": "Supply Chain",
            "tagColor": "bg-blue-100 text-blue-700",
            "date": current_date,
            "title": "供应链情报：CoWoS 产能扩充加速",
            "summary": f"台积电宣布在嘉义科学园区增设封装厂，预计提升产能 {random.randint(15, 30)}% 以应对 GPU 缺货。",
            "source": "Digitimes"
        },
        {
            "url": "#",
            "category": "Consumer",
            "tagColor": "bg-purple-100 text-purple-700",
            "date": current_date,
            "title": "RTX 5090 显卡规格泄露：显存位宽大幅提升",
            "summary": "知名爆料人称，下一代旗舰显卡将采用 512-bit 显存位宽，带宽突破 2TB/s。",
            "source": "Videocardz"
        },
        {
            "url": "#",
            "category": "Policy",
            "tagColor": "bg-red-100 text-red-700",
            "date": current_date,
            "title": "半导体出口管制新规解读",
            "summary": "商务部发布最新指导意见，加强对高性能计算芯片的合规审查。",
            "source": "Reuters"
        }
    ]
    return news_items

def save_to_js(data):
    # 生成 data.js
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    # 关键：这里生成的变量名必须和 HTML 里的引用一致 (newsData)
    js_content = f"const newsData = {json_str};"
    
    with open("data.js", "w", encoding="utf-8") as f:
        f.write(js_content)
    print("✅ data.js 自动化生成完毕")

if __name__ == "__main__":
    news = fetch_news()
    save_to_js(news)

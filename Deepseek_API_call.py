import json
import os
from openai import OpenAI

with open('ANN_news_data.json', 'r', encoding='utf-8') as myFile:
    news_list = json.load(myFile)
print("successfully loaded", {len(news_list)}, "pieces of news")

client = OpenAI(
    api_key= os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

API_json = []

for i in range (len(news_list)):
    news_text = json.dumps(news_list[i], ensure_ascii = False, indent = 2)
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "你是一个专业的动漫资讯筛选助手，判断标准偏宽松.任务分两步.\n"
                                    "第一步：根据用户喜欢的作品类型，筛选出符合偏好的新闻。\n"
                                    "用户喜欢的作品类型：百合恋爱（非常喜爱）；以通往夏天的隧道，再见的出口，你的名字，天气之子为代表的情感驱动型奇幻（非常喜爱，但不包括涉及巫女，神社，法术等元素的奇幻）；男女恋爱；以孤独摇滚，我心里危险的东西等为代表的少女乐队，校园题材\n"
                                    "可能喜欢：现实题材的，以我推的孩子为代表的悬疑复仇，成人恋爱的现实治愈，以及以间谍过家家为代表的喜剧题材\n"
                                    "几乎不看：耽美；以海贼王，鬼灭之刃为代表的战斗，玄幻冒险题材；以灌篮高手，排球少年为代表的体育;真人电影题材\n"
                                    "第二步：仅当新闻属于上述'喜爱'或'可能喜欢'的类型时，再判断它是否属于重大公告。\n"
                                    "重大公告的定义：\n"
                                    "1.动画开播，漫画，轻小说发行决定"
                                    "2. 动画续作（第二季、第三季、Finale 等）制作决定，或漫画，轻小说等上架决定\n"
                                    "3. 全新动画化（TV动画、剧场版）企划公布。\n"
                                    "4. 制作委员会或官方发布的关键视觉图（KV）、预告 PV 或具体上映日期。\n"
                                    f"返回格式必须严格为JSON：\n"
                                    f"{{\"is_important\": true/false, \"summary\": \"若重要则用活泼自然语气写100-200字的概括（而非生硬的摘要），概括中作品名严格使用原文，不要翻译。注意不用写”符合用户偏好“之类的推送理由。若不重要则严格填空字符串\"}}\n\n"
                                    f"The news data is as follows:\n{news_text}"}
    ]

    response = client.chat.completions.create(
        model = "deepseek-v4-flash",
        messages = messages,
        stream = False,
        extra_body = {"thinking": {"type": "disabled"}},
        temperature = 0.5
    )
    print(response.choices[0].message.content)
    API_json.append(response.choices[0].message.content)

try:
    with open('API_data.json', 'w', encoding='utf-8') as myFile:
        json.dump( API_json , myFile, ensure_ascii = False, indent=2)
    print("API_data file writing complete")
except Exception as e:
    print(f"API_data file writing fail: {e}")

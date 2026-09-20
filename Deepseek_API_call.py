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

with open("prompt.txt", "r", encoding="utf-8") as f:
    prompt = f.read()

for i in range (len(news_list)):
    news_text = json.dumps(news_list[i], ensure_ascii = False, indent = 2)
    messages = [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": prompt + "\n"+ news_text}
    ]

    response = client.chat.completions.create(
        model = "deepseek-flash",
        messages = messages,
        stream = False,
        reasoning_effort="low",
        extra_body={"thinking": {"type": "enabled"}},
        response_format={"type": "json_object"}
    )
    print(response.choices[0].message.content)
    API_json.append(response.choices[0].message.content)

try:
    with open('API_data.json', 'w', encoding='utf-8') as myFile:
        json.dump( API_json , myFile, ensure_ascii = False, indent=2)
    print("API_data file writing complete")
except Exception as e:
    print(f"API_data file writing fail: {e}")

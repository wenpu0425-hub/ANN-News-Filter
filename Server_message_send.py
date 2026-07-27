import json
import requests
import os

with open('API_data.json', 'r', encoding='utf-8') as myFile:
    summary_list = json.load(myFile)
print("successfully loaded", len(summary_list), "pieces of news")

summary = ""
j=0
for i in range (len(summary_list)):
    my_dict = summary_list[i]
    real_dict = json.loads(my_dict)
    if(real_dict["is_important"] == True):
        j += 1
        if j > 1:
            summary += "\n\n"
        summary += f"第{j}条新闻"
        summary += "—————————————————————————————"
        summary += real_dict["summary"]

summary_split = summary.split("\n\n")
interval = 5
for i in range (0 , len(summary_split) , interval):
    url = os.getenv("Server_Key")
    summary_prosseing = summary_split[i : i+ interval]
    summary_final = "\n\n".join(summary_prosseing)
    params = {
        "title": "动漫三天报告",
        "desp": summary_final
    }
    response = requests.post(url, params=params)

    if response.status_code == 200:
        print("Push successful")
    else:
        print("Push failed:", response.text)

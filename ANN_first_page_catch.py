from bs4 import BeautifulSoup
from datetime import date,timedelta
import requests
import textwrap
import json

def fetch_link_and_time():
    dict = {}
    lst_link = []
    lst_time = []
    head = {"User-Agent": "Mozilla/5.0"}
    response = requests.get("https://www.animenewsnetwork.com/",headers=head)
    if response.status_code >= 300:
        print("connection of article fetching failed, status_code:", response.status_code)
    elif 200 <= response.status_code < 300:
        content = response.text
        print("connection of article fetching succeeded, status_code:", response.status_code)

        soup = BeautifulSoup(content, "html.parser")
        all_link_wraps = soup.find_all("div", class_="wrap") #寻找链接填充lst_link
        for link_wrap in all_link_wraps:
            a_tag = link_wrap.find("a")
            if a_tag.get("href"):
                link = a_tag["href"]
                if link != "":
                   original_link="https://www.animenewsnetwork.com" + link
                   lst_link.append(original_link)
                else: print("link catch error")

        all_time_wraps = soup.find_all("div", class_="byline")
        for time_wrap in all_time_wraps:
            time_tag = time_wrap.find("time")
            if time_tag.get("datetime"):
                times = time_tag["datetime"]
                if times != "":
                    times_split = times.split("T")
                    original_times = times_split[0]
                    lst_time.append(original_times)
                else: print("time catch error")

        for i in range (len(lst_link)):
           dict[lst_link[i]] = lst_time[i]
    return dict

def fetch_news_article(link):
    headline_and_article = []
    head={"User-Agent":"Mozilla/5.0"}
    response = requests.get(link,headers=head)
    if response.status_code >= 300:
        print("connection of article fetching failed, status_code:", response.status_code)
    elif 200 <= response.status_code < 300:
        content = response.text
        soup = BeautifulSoup(content,"html.parser")
        all_article_name = soup.find_all("div",attrs={"class":"meat"})
        for article_name in all_article_name:
            headline_and_article.append(article_name.get_text(separator = " ",strip = True))

        h1 = soup.find("h1", id="page_header")
        title = h1.get_text(" ", strip=True)
        title = title.replace("News ", "", 1)
        headline_and_article.append(title)

        return headline_and_article


if __name__ == "__main__":
    today = date.today()
    three_days_ago = today - timedelta(days=3)

    dict = fetch_link_and_time()
    my_json = []

    lst_link = list(dict.keys())
    lst_time = list(dict.values())

    for i in range (len(lst_link)):
        result = lst_link[i].split("/")
        if result[3] == "news":
            article_date = date.fromisoformat(lst_time[i])
            if three_days_ago <= article_date <= today:
                headline_and_article = fetch_news_article(lst_link[i])
                my_dict = {"URL": lst_link[i], "Date": lst_time[i], "Title": headline_and_article[1], "Content": headline_and_article[0]}
                my_json.append(my_dict)

    with open('ANN_news_data.json', 'w', encoding='utf-8') as myFile:
        json.dump( my_json , myFile, ensure_ascii = False, indent=2)

    print("successfully install", {len(my_json)} ,"pieces of news to ANN_news_data.json")
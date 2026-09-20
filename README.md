# ANN-News-Filter
A simple handwritten program that filters news at ANN's homepage based on Deepseek API, and pushes matched results to ServerChan. You can edit the prompt in prompt.txt according to your own interests.

一个手写的简单程序，通过 DeepSeek API 筛选 ANN 首页上的新闻，并把匹配到的结果推送到 ServerChan（Server 酱）。你可以根据自己的兴趣修改 prompt.txt 里的提示词。

## 推送流程
ANN 首页
↓
抓取近三天的新闻
↓
保存为 ANN_news_data.json
↓
DeepSeek API 分析新闻
↓
根据 prompt.txt 判断新闻是否值得关注
↓
保存筛选结果
↓
Server酱推送重要新闻

## 文件说明
ANN_first_page_catch.py
负责从 ANN 首页抓取新闻链接、日期、标题和正文，并保存到 ANN_news_data.json。

Deepseek_API_call.py
读取新闻数据，调用 DeepSeek API 对每条新闻进行分析，并保存 API 返回结果。

Server_message_send.py
读取 DeepSeek 的分析结果，将被标记为重要的新闻整理后，通过 Server酱推送。

prompt.txt
DeepSeek 使用的提示词。
可以直接修改这里的内容，使新闻筛选标准符合自己的兴趣。

requirements.txt
项目运行所需要的 Python 第三方库。

.github/workflows/anime_news.yml
GitHub Actions 工作流，用于定时自动运行程序。

## 环境要求
Python 3.13
需要安装以下 Python 库：
pip install -r requirements.txt

同时需要准备：
1. DeepSeek API Key
2. Server酱 SendKey
3. 可以正常访问 Anime News Network 的网络环境

## 自定义新闻筛选
项目的筛选规则主要写在 prompt.txt 中。

你可以根据自己的兴趣修改提示词，例如指定：

- 喜欢的动画作品
- 喜欢的声优
- 喜欢的制作公司
- 对哪些类型的新闻更感兴趣
- 哪些新闻应该忽略

程序本身不固定新闻筛选标准，主要由 prompt.txt 决定。

## 运行方式
按照以下顺序运行：
python ANN_first_page_catch.py

python Deepseek_API_call.py

python Server_message_send.py

三个程序分别完成：
抓取新闻 → AI 筛选 → 推送结果

## GitHub Actions
项目包含 GitHub Actions 工作流，可以让程序在云端按照设定的时间自动运行。因此不需要每天手动打开电脑运行 Python。

使用 GitHub Actions 时，需要在 GitHub Repository 的 Secrets 中配置：DEEPSEEK_API_KEY 和 SERVER_KEY

具体运行时间可以在：.github/workflows/anime_news.yml中修改。

## 已知限制
这是一个个人学习项目，因此仍然存在一些限制：

- 新闻抓取依赖 ANN 首页的网页结构，因此 ANN 修改网页结构后，爬虫可能失效
- 新闻日期按照 ANN 页面提供的数据进行处理
- DeepSeek 的筛选结果依赖 prompt 和模型判断
- 每条新闻都需要调用一次 API，因此新闻数量增加后 API 使用量也会增加
- 网络环境可能影响 ANN 的访问
- 项目目前主要针对个人使用，没有设计复杂的错误处理和高并发机制

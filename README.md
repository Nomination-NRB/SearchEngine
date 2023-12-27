# 新闻搜索引擎
简易的搜索引擎

![8eec58c0965eff97c00b47f13a605b8](https://github.com/Nomination-NRB/SearchEngine/assets/83486284/9a18ea47-c2ba-471e-a021-1daf637ac212)

![e19ae8bc4976db93b8f7a96e5ffc959](https://github.com/Nomination-NRB/SearchEngine/assets/83486284/8b6eaa62-3059-47b3-9c46-4423948946b2)


## 技术栈

前端：HTML，Django语法

后端：flask

数据库：sqlite3

## 基本功能

- 检索模块
  - 单词检索：北京
  - 多词检索：北京 奥运会
  - 句子检索：我要去北京看奥运会
- 排序模块
  - 相关度排序
  - 热度排序
  - 时间排序
- 搜索条件扩展
  - 搜索深圳，会提示广州，宝安区等信息
- 搜索结果得分
  - 每一个结果标题后面会有得分，分数越高越好
- 搜索词高亮
- 搜索内容分行
- 推荐阅读
- 整套UI界面

## 数据来源

公开的新闻数据：250万篇新闻，2014-2016年
链接: https://pan.baidu.com/s/16wXK8YgJzGnrDTn6ffjmEg 提取码: cvj3
json格式：title标题，content正文，keywords关键词，desc描述，source来源

```json
{	"news_id": "610130831",
	"keywords": "导游，门票",
	"title": "故宫淡季门票40元 “黑导游”卖外地客140元",
	"desc": "近日有网友微博爆料称，故宫午门广场售票处出现“黑导游”，专门向外地游客出售高价门票。昨日，记者实地探访故宫，发现“黑导游”确实存在。窗口出售",
	"source": "新华网",
	"time": "03-22 12:00",
	"content": "近日有网友微博爆料称，故宫午门广场售票处出现“黑导游”，专门向外地游客出售高价门票。昨日，记者实地探访故宫，发现“黑导游”确实存在。窗口出售40元的门票，被“黑导游”加价出售，最高加到140元。故宫方面表示，请游客务必通过正规渠道购买门票，避免上当受骗遭受损失。目前单笔门票购买流程不过几秒钟，耐心排队购票也不会等待太长时间。....再反弹”的态势，打击黑导游需要游客配合，通过正规渠道购买门票。"
}
```


## 目录

```
searchEngine
├─ README.md·································//项目介绍
├─ requirements.txt··························//项目依赖库
├─ code
│    ├─ convert_json_to_xml.py···············//将json数据提取并转换为对应格式的xml
│    ├─ index_module.py
│    ├─ recommendation_module.py
│    └─ setup.py·····························//构建倒排索引以及推荐阅读(用index_module.py与recommendation_module.py)
├─ config.ini································//路径配置文件，根据需要进行修改
├─ data
│    ├─ idf.txt······························//计算的词频
│    ├─ ir.db································//数据库文件(每次执行setup.py都会重写里面的数据)
│    ├─ learning_source
│    │    └─ sgns.sogounews.bigram-char······//扩展搜索需要的词库
│    ├─ new_xml······························//本地xml文件，此处只列出5个
│    │    ├─ 1.xml
│    │    ├─ 10.xml
│    │    ├─ 100.xml
│    │    ├─ 1000.xml
│    │    ├─ 1001.xml
│    └─ stop_words.txt·······················//停用词
└─ web
       ├─ main.py····························//执行总文件
       ├─ search_engine.py···················//测试三种排序得分
       ├─ static·····························//静态UI图片
       │    ├─ abstract.jpg
       │    ├─ duck.png
       │    ├─ shark.png
       │    ├─ sleep.jpg
       │    ├─ star.png
       │    ├─ warma3.jpg
       │    └─ warma_happy.jpg
       └─ templates··························//前端文件(Django语法)
              ├─ content.html
              ├─ high_search.html
              ├─ next.html
              └─ search.html
```



## 使用方法

```
git clone https://github.com/Nomination-NRB/SearchEngine
```

在vscode或者其他编译器打开项目文件夹

激活本项目具体使用的环境，切换到requirements.txt目录下在终端执行该命令即可

```
pip install -r requirements.txt
```

**注意注意注意**：词汇扩展所需的词库需要自己下载：[词库](https://pan.baidu.com/s/1svFOwFBKnnlsqrF1t99Lnw)

下载后将文件解压放到路径：**searchEngine/data/learning_source/**

## 运行

1. 使用现成数据库里的数据
   1. 运行main.py文件，打开本地链接即可（由于使用词库扩展搜索，运行时间较长，第一次运行大概1-2min）
2. 使用自己的数据
   1. 根据自己的数据特点，将数据存储到xml文件中（可以参考convert_json_to_xml.py）
   2. 运行setup.py构建倒排索引，推荐阅读，更新词频，数据库文件
   3. 运行main.py文件，打开本地链接即可（由于使用词库扩展搜索，运行时间较长，第一次运行大概1-2min）

## 参考

[01joy/news-search-engine: 新闻搜索引擎 (github.com)](https://github.com/01joy/news-search-engine)






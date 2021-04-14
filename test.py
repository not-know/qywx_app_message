from qywx_app_message import *


# 企业id，在这里获取 https://work.weixin.qq.com/wework_admin/frame#profile 最下面的企业ID就是
corpid = ""
# 在应用管理最下面新建应用
# 创建好后打开引用界面，agentid就是
agentid = ""
# 点击 Secret的查看
# 在点击 发送Secret到企业微信中查看，然后在企业微信中查看
corpsecret = ""

# 生成实例
wxclient = qywx_app_message(corpid, agentid, corpsecret)

# 实例化后，可以设置是否开启检查重复消息，
# 在一定时间内重复的消息将不再发送
# 0：关闭， 1：开启    默认0
wxclient.check = 0

# 多长时间内重复消息不发送，默认1800s
wxclient.check_time = 1800

# 设置发送的范围，用户（user）、部门（party）、标签（tag）
# 需要是可遍历的对象，列表元组之类的
# 不设置的话是发给应用的所有可见人
wxclient.send_range(user=["test"])
# print(wxclient.data)

# 发送文本消息，
# 第一个是企业应用id，在应用管理，找到想要发消息的应用
text = """cs上线提醒，赶紧去看看吧

ip地址:          127.0.0.1
计算机名:      DESKTOP-XXXXXXX
用户名:          administrator
"""
r = wxclient.send_text(text)

# 发送卡片消息
r = wxclient.send_textcard("新抓取到的 CVE 已到达",
                           "爬取到的 README.md 内容\r\n此exp相当危险可日天日地日一切\r\n\r\n点击卡片跳转到项目页面", "https://github.com/")

# 图文消息最少一条，第一条的图片是大图，官网说 1068*455（差不多21:9） 显示效果会好一点。
# 如果只有标题和描述显示的效果卡片消息一样
news = [{"title": "xxxxx番更新了", "description": "描述",
         "url": "https://www.bilibili.com/anime/timeline/", 
         "picurl": "https://image.zhr.red/images/2021/04/14/image-2021-04-14-18-21-44-108884.md.png"}]

# 后面的都是小图，最多支持8条，小图150*150 显示效果会好一点
news.append({"title": "xxxxxxxxx", "description": "描述",
             "url": "https://www.bilibili.com/anime/timeline/", 
             "picurl": "https://image.zhr.red/images/2021/04/14/9b2fadeebea37c5da20ec9215fc4056caee69584.png"})
news.append({"title": "xxxxxxxxx", "description": "描述",
             "url": "https://www.bilibili.com/anime/timeline/", 
             "picurl": "https://image.zhr.red/images/2021/04/14/9b2fadeebea37c5da20ec9215fc4056caee69584.png"})
news.append({"title": "xxxxxxxxx", "description": "描述",
             "url": "https://www.bilibili.com/anime/timeline/", 
             "picurl": "https://image.zhr.red/images/2021/04/14/9b2fadeebea37c5da20ec9215fc4056caee69584.png"})

# 发送图文消息
r = wxclient.send_news(news)

# markdown 文本
markdown = """
# 一级标题
## 二级标题
### 三级标题
#### 四级标题
##### 五级标题
###### 六级标题

## 特殊字体
*斜体*              
**粗体**            __粗体__
***加粗斜体***      ___加粗斜体___
~~删除线~~
## 缩进
+ 缩进
  + 层级缩进（记得+之间有空格） 
    + 多层
## 引用
> 引用

## 链接
[链接](https://www.baidu.com)

## 无序文本
- 文本1
- 文本2
- 文本3
## 有序文本
1. 文本1
2. 文本2
3. 文本3
## 代码
```python
while
    print("无限起飞")
```
`代码片段`

## 颜色
<font color="info">绿色</font>
<font color="comment">灰色</font>
<font color="warning">橙红色</font>
"""
# 发送 markdown 消息
r = wxclient.send_markdown(markdown)

# 有什么问题可以直接看响应，返回的就是requests模块的响应
if r.json()["errmsg"] != "ok":
    print(json.dumps(r.json(), indent=4, ensure_ascii=False))
    print("\r\n\r\n可以查看官方错误代码：")
    print("https://work.weixin.qq.com/api/doc/90000/90139/90313")

import requests
import json
import re


class qywx_app_message:
    """发送应用消息

    官网文档 企业微信应用消息发送
    https://work.weixin.qq.com/api/doc/90000/90135/90236

    官网文档 错误代码
    https://work.weixin.qq.com/api/doc/90000/90139/90313
    """

    def __init__(self, corpid: str, agentid: int, corpsecret: str):
        """
        corpid      企业 ID
        agentid     应用 ID
        corpsecret  应用 Secret
        """

        # 企业ID
        self.corpid = corpid
        # 应用 Secret
        self.corpsecret = corpsecret
        # 消息模板
        self.data = {
            "touser": "@all",
            "agentid": agentid,
            "msgtype": "text",  # 消息类型
        }
        # 是否开启检查重复消息，在一定时间内重复的消息将不再发送
        # 0：关闭， 1：开启    默认0
        self.check = 0
        # 多长时间内重复消息不发送，默认1800s
        self.check_time = 1800

    def get_access_token(self):
        """获取access_token

        access_token 有效期
        有效期为两个小时，两个小时内重新获取access_token也不会变，
        企业微信每次重新获取就好了
        https://developers.weixin.qq.com/community/enterprisewechat/doc/000e025b13c3f8ae344a78f1256400

        获取 access_token 官网文档
        https://work.weixin.qq.com/api/doc/90000/90135/91039
        """
        corpid = self.corpid
        corpsecret = self.corpsecret
        url = f"https://qyapi.weixin.qq.com//cgi-bin/gettoken?corpid={corpid}&corpsecret={corpsecret}"
        r = requests.get(url)
        # 判断时候获取 access_token 成功，失败退出脚本
        if r.json()["errmsg"] != "ok":
            print("获取access_token失败，请检查企业ID和Secret是否正确：")
            self.wxerror(r)
        access_token = r.json()["access_token"]
        return access_token

    def wxerror(self, r):
        """显示错误消息的"""
        print(json.dumps(r.json(), indent=4, ensure_ascii=False))
        print("\r\n\r\n可以查看官方错误代码：")
        print("https://work.weixin.qq.com/api/doc/90000/90139/90313")
        exit(0)  # 退出程序

    def send_range(self, user: list = None, party: list = None, tag: list = None) -> dict:
        """指定发送消息的范围，默认是发给应用的可见范围里所有人

        user        发送的用户
        party	    发送的部门
        tag         发送的标签，管理员可以创建标签

        需要类型都是可遍历的
        """

        to_list = {"toparty": party, "totag": tag, "touser": user}

        for k in ["toparty", "totag", "touser"]:
            # 判断是不是空
            if to_list[k]:
                if "touser" in self.data.keys():
                    # 把默认的发给所有人删掉
                    del self.data['touser']
                if "@all" in to_list[k]:
                    # 如果有@all，就设为@all
                    self.data.update({k: "@all"})
                else:
                    self.data.update({k: "|".join(to_list[k])})

    def _send(self, json=None):
        """发送消息"""
        # 获取access_token
        access_token = self.get_access_token()

        # 消息重复检查是否开启设置
        json.update({"enable_duplicate_check": self.check,
                    "duplicate_check_interval": self.check_time})

        # 发送消息
        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={access_token}"
        r = requests.post(url=url, json=json)
        return r

    def send_text(self, text: str) -> requests.Response:
        """发送文本消息

        content		消息内容，超过2048字节会分段发送

        可以支持超链接消息，示例：
        “百度都不会吗\r\n<a href=\"http://www.baidu.com\">百度一下</a>”
        """
        data = self.data
        # 添加消息的内容
        data.update({"text": {"content": text}})

        # 判断是否长度超过2048，超过2048分段发送
        if len(text) > 2048:
            data_list = re.findall(r".{1,2048}", text)
            data_list.append("因为消息超过2048字节")
            for data_text in data_list:
                data.update({"text": {"content": data_text}})
                r = self._send(data)
        else:  # 不是就直接发送
            r = self._send(data)

        # 只返回最后一个响应
        return r

    def send_textcard(self, title: str, desc: str, url: str, btntxt: str = None) -> requests.Response:
        """发送卡片消息
            title：     标题，不超过128个字节，超过会自动截断
            desc：      描述，不超过512个字节，超过会自动截断
            url：       点击后跳转的链接。最长2048字节，请确保包含了协议头(http/https)
            btntxt：    按钮文字。 默认为“详情”， 不超过4个文字，超过自动截断。非必须
            
        官网字体颜色说明
        特殊说明：
        卡片消息的展现形式非常灵活，支持使用br标签或者空格来进行换行处理，
        也支持使用div标签来使用不同的字体颜色，目前内置了3种文字颜色：
        灰色(gray)、高亮(highlight)、默认黑色(normal)，
        将其作为div标签的class属性即可，具体用法请参考上面的示例。
        """
        data = self.data
        # 更改为卡片类型
        data.update({"msgtype": "textcard"})
        # 添加消息的内容
        data.update({"textcard": {"title": title,
                                  "description": desc,
                                  "url": url,
                                  "btntxt": btntxt
                                  }})

        r = self._send(data)
        return r

    def send_news(self, news: list) -> requests.Response:
        """发送图文消息
            articles	    图文消息，一个图文消息支持1到8条图文，
            title		    标题，不超过128个字节，超过会自动截断（支持id转译）
            desc    		描述，不超过512个字节，超过会自动截断（支持id转译）
            url	        	点击后跳转的链接。 最长2048字节，请确保包含了协议头(http/https)
            picurl	    	图文消息的图片链接，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150。
                            图片链接可以为空，为空的时候和卡片消息一样。

        title和description是必需值，没有不行，另外两个连接可以没有，显示的效果会和卡片消息类似
        """
        # 复制消息模板
        data = self.data
        # 更改为图文类型
        data.update({"msgtype": "news"})

        # 创建图文内容列表
        articles = []

        # 添加消息的内容
        for n in news:
            if ("title" in n.keys()) and ("description" in n.keys()):
                # 写入标题 和 描述
                article = {"title": n["title"],
                           "description": n["description"]}

                if "url" in n.keys():
                    # 如果存在 url 就写入
                    article.update({"url": n["url"]})

                if "picurl" in n.keys():
                    # 如果存在 图片链接 就写入
                    article.update({"picurl": n["picurl"]})
            else:
                print("title和description是必需值，没有不行")
                exit()

            # 添加条目
            articles.append(article)

        # 添加消息的内容
        data.update({"news": {"articles": articles}})

        r = self._send(data)
        return r

    def send_markdown(self, text: str) -> requests.Response:
        """发送markdown消息

        text		消息内容，超过2048字节后面的会删掉

        目前微信上是看不了的，只有上企业微信才可以看到（2021年4月14日）
        """
        data = self.data
        # 更改为 markdown 类型
        data.update({"msgtype": "markdown"})
        # 添加消息的内容
        data.update({"markdown": {"content": text}})

        r = self._send(data)
        return r


if __name__ == "__main__":
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
    r = wxclient.send_text("cs上线提醒")

    # 发送卡片消息
    r = wxclient.send_textcard("新抓取到的 CVE_EXP 已到达",
                               "爬取到的 README.md 内容\r\n\r\n\r\n点击卡片跳转到项目页面", "https://github.com/")

    # 图文消息最少一条，第一条的图片是大图，官网说 1068*455（差不多21:9） 显示效果会好一点。
    # 如果只有标题和描述显示的效果卡片消息一样
    news = [{"title": "xxxxx番更新了", "description": "描述",
             "url": "https://www.bilibili.com/", "picurl": "http://图片链接"}]

    # 后面的都是小图，最多支持8条，小图150*150 显示效果会好一点
    news.append({"title": "xxxxxxxxx", "description": "描述",
                 "url": "https://www.bilibili.com/", "picurl": "http://图片链接"})
    news.append({"title": "xxxxxxxxx", "description": "描述",
                 "url": "https://www.bilibili.com/", "picurl": "http://图片链接"})
    news.append({"title": "xxxxxxxxx", "description": "描述",
                 "url": "https://www.bilibili.com/", "picurl": "http://图片链接"})

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

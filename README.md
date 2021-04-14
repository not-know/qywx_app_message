<h1 align="center"> qywx_app_message </h1>


<br/>

## 说明

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;只要注册一个企业微信就可以使用了，并且还是免费的不用验证主体就可以使用，但需要实名认证，这里需要注意一点，权限什么的一定要设置好（企业不可以被搜到，别名要打开等设置）。比较好的就是直接关注自己企业的微信公众号，就可以通过微信API推送消息了，还可以在聊天栏置顶，消息不会错过，并且可以添加多个应用来推送不同的消息。美滋滋啊，芜湖起飞。

<br/>

推送企业微信应用消息，解决了我以下不爽的地方：
<br/>

  +  server酱只能推送卡片消息，实在是难受的不行
  +  server酱每次还要打开一个网页，使用电脑的默认浏览器打开还会提醒用微信内置浏览器才可以打开
  +  其他的py模块都太过于臃肿，还用不明白，我就只是想推送个消息而已啦~
  +  还有很多都是半成品。被逼无奈只能自己动手。
  +  而且还能白嫖腾讯，白嫖腾讯会让我感觉小时候赔的都赚回来了，滑稽.jpg

<br/>

## 使用
1. [注册企业微信](https://work.weixin.qq.com/wework_admin/register_wx?from=myhome)

   ![image-20210414224357906](https://image.zhr.red/images/2021/04/14/image-2021-04-14-22-43-58-774745.png)

2. 注册完成后登录到后台，点击应用管理，创建新应用。也可以直接打开这个链接 => [创建应用](https://work.weixin.qq.com/wework_admin/frame#apps/createApiApp)

      ![image-20210414224657834](https://image.zhr.red/images/2021/04/14/image-2021-04-14-22-46-58-734637.png)

3. 点击查看

      ![image-20210414225147353](https://image.zhr.red/images/2021/04/14/image-2021-04-14-22-51-48-216390.png)

4. 点击发送，然后这个只能到企业微信中看， 需要手机下载企业微信
   
   ![image-20210414225333987](https://image.zhr.red/images/2021/04/14/image-2021-04-14-22-53-34-841672.png)
   
5. 最后打开我的企业最下面，找到企业id   https://work.weixin.qq.com/wework_admin/frame#profile

      ![image-20210414225615724](https://image.zhr.red/images/2021/04/14/image-2021-04-14-22-56-16-620281.png)

      

6. 这样我们就有了企业ID、应用ID、应用Secret，已经可以发送消息了

7. 最后还要关注一下企业的公众号，打开这个[链接](https://work.weixin.qq.com/wework_admin/frame#profile/wxPlugin)然后扫码关注，这样你就可以收到消息了   

      ![image-20210415004752679](https://image.zhr.red/images/2021/04/14/image-2021-04-15-00-47-53-405734.png)

8. 使用pip安装模块, 也可以直接复制粘贴出去，一共才一百多行代码（但是需要安装requests模块）

      ```python
      pip3  install qywx-app-message
      ```

9. 打开`python`发送一个测试消息，只要你没填错，就可以发消息了

      ```python
      from qywx_app_message import *
      
      
      # 企业ID
      corpid = "xxxxxxxxxxxxxxxxxx"
      # 应用ID
      agentid = "1000002"
      # 应用Secret
      corpsecret = "xxxxxxxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxx"
      wxclient = qywx_app_message(corpid, agentid, corpsecret)

      wxclient.send_text("测试消息")
      ```


9. 这时你就发现你多了一条消息

      ![1](https://image.zhr.red/images/2021/04/14/image-2021-04-15-00-28-56-362503.gif)

      

      

      ### 还可以发多种类型的消息，下面是示例

      + 文本

        ![image-20210415003241462](https://image.zhr.red/images/2021/04/14/image-2021-04-15-00-32-42-151542.png)

      + 卡片

        ![image-20210415003317372](https://image.zhr.red/images/2021/04/14/image-2021-04-15-00-33-57-828130.png)

      + 图文（图文支持1-8条，这个是四条的。第一条是大图，后面都是小图）

        ![image-20210415003351480](https://image.zhr.red/images/2021/04/14/image-2021-04-15-00-33-52-198897.png)

      + markdown（目前只支持企业微信端的，微信上看不了）

        ![image-20210415003531290](https://image.zhr.red/images/2021/04/14/image-2021-04-15-00-35-31-977325.png)

        ![image-20210415003629682](https://image.zhr.red/images/2021/04/14/image-2021-04-15-00-36-30-517140.png)

      <br/><br/>

      ## [示例响应的代码](test.py)

      **指定发送范围和消息重复也是有的，可以看下面示例**
      
      ```python
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
                                 "爬取到的 README.md 内容\r\n此exp相当危险可日天日地日一切\r\n\r\n点击卡片跳转到项目页面", 
                                 "https://github.com/")
      
      
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
      ​```python
      while
          print("无限起飞")
      ​```
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
      ```
      
      <br/><br/>
      
      ## cs的插件示例  -还想研究
    
      <br/><br/>
      
      ## cve推送示例   -还想研究
    
      <br/><br/>
      ## 微信   欢迎大佬来指导，嘤嘤嘤
      ![image-20210415011447889](https://image.zhr.red/images/2021/04/14/image-2021-04-15-01-14-48-599780.png)

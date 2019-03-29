## Blog
基于Django2搭建的个人博客网站

访问地址：[永春小站](http://www.yooongchun.com)

本文介绍如何使用`Django` 从零开始搭建一个专属自己的高度定制化的博客平台。

---

## 1.网站示例

你可以到这里查看博主的博客示例：[永春小站](http://www.yooongchun.cn)

`Github`项目地址：https://github.com/yooongchun/Blog

网站特点：

- 基于`Bootstrap4` ，响应式布局
- 卡片式展现，美观易读
- 支持`Markdown` 语法

- 网站主页示例：

  ![](https://yooongchun-blog.oss-cn-hangzhou.aliyuncs.com/blog-web-blog/screencapture-yooongchun-cn-1549810389940.png)

## 2.技术概要

完成本站建设，你需要以下技能：

前端：

- `HTML5`
- `Bootstrap4`
- `CSS3`
- `JAVASCRIPT/jQuery` 
- `Django2`

后端：

- `Python3`
- `云服务器部署`

如果以上哪个部分你未掌握，可根据以下推荐酌情学习！

关于前端的学习，我的建议是快速学习一遍这里的教程，了解什么功能用什么方式实现即可：

- 菜鸟教程：[Bootstrap](http://www.runoob.com/bootstrap4/bootstrap4-tutorial.html)
- 菜鸟教程：[Javascript](http://www.runoob.com/js/js-tutorial.html)
- 菜鸟教程：[jQuery](http://www.runoob.com/jquery/jquery-tutorial.html)
- 菜鸟教程：[HTML](http://www.runoob.com/html/html-tutorial.html)
- 菜鸟教程：[CSS](http://www.runoob.com/css/css-tutorial.html)
- `Django`教程：[编写你的第一个Django应用](https://docs.djangoproject.com/zh-hans/2.1/intro/tutorial01/)，看完一至七即可

关于后端，建议学习以下教程：

- `Python3` 学习：[廖雪峰的Python3教程](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)
- `云服务器部署`：本文后面会有讲解

## 3.开始建站

### 3.1新建Django工程

我们的站点，从建立一个`Django` 工程开始，博主这里选择的是`Pycharm` 来进行开发，需要注意的是`Pycharm` 教育版是不支持创建`Django` 项目的，需要使用专业版。按以下步骤创建一个`Django`工程：

```shell
File->New Project->Django->mysite
```

以上最后一项代表取名为：`mysite`

现在，我们的工程目录如下：

```shell
mysite
	|-mysite
		|-__init__.py
		|-settings.py
		|-urls.py
		|-wsgi.py
	|-templates
	|-manage.py
```

首先，新建一个自己的应用，命名为`blog`，此时工程目录如下：

```shell
mysite
	|-blog
	|-mysite
		|-__init__.py
		|-settings.py
		|-urls.py
		|-wsgi.py
	|-templates
	|-manage.py
```

按照上面介绍的`Django`教程进行内容开发。首先根据你的需求确定数据库的表内容，博主的数据库表包括：`Image`、 `User`、 `Category`、 `TagProfile`、 `InfoMsg` 、`Blog`、 `Visitor`、 `Comment`、 `Message`、 `Resource`、 `FriendLink`；分别存储的内容是：图片【包括文章封面图和用户头像图】、用户信息、博客分类、标签、网站通知信息、博文内容、访客信息、留言、评论、资源和友情链接信息。

 接下来开始编写`Views.py` ，包括`Index` 、`About`、`Articles` 、`Archive` 、`MessageInfo`、`Search`、`Detail`、`ResourceInfo`、`Approval`、`ApplyFriendLink`和`Sponsor` 几个类，分别对应的功能是：首页、关于页、文章列表页、归档页、留言信息页、搜索页、文章详情页、资源信息页、点赞功能、申请友链和捐赠页。

接着按照`Views.py` 对应的类来开发相应的`html` 页面。`Index` 类对应`index.html`，`About` 类对应`about.html` ，依次对应。其中有些部分会用到多次，这时将其单独分离出来作为模块调用，包括：`article-footer.html` 模块提供文章底部信息，如下图示意：

![](https://yooongchun-blog.oss-cn-hangzhou.aliyuncs.com/blog-web-blog/WeChat%20Screenshot_20190215145249.png)

`article-list.html` 模块提供卡片式文章列表展示；其余的模块功能跟其名称差不多，非常容易理解。`html` 文件对应的样式则单独分离出来，放在`static/blog/css/public.css`文件中，对应的`js`文件放在`static/blog/js`目录下，其中`approve.js` 负责点赞效果呈现及提交点赞请求，`comment.js` 负责评论内容提交，`friend-link.js`负责申请友链请求的提交，`message.js` 负责留言信息提交，`public.js`则负责一些公用的逻辑，`nav-loop-message.js` 负责导航栏的循环滚动消息，`resource.js`负责资源信息逻辑处理，`site-map-figure.js`负责关于页面的站点访问信息地图绘制，`editormd.js`是引入的`editor.md`插件的调用，`css/editor.min.css`则是相应的样式渲染文件。

另外，值得提一下的是`elusive-icons.min.css`是引入的第三方插件，用来提供站点图标，具体情况可访问官网：http://elusiveicons.com/icons/

最后，只需要将我们撰写的页面内容通过`urls.py` 文件来进行转发就行了。 完成后即可运行一下看看效果了。

在本地把内容调整好后，需要把我们的博客部署到服务器上。

### 3.2在服务器上部署Django工程

把`Django` 工程部署到服务器上，使用`nginx`+`uwsgi` 两个工具，参考链接：http://www.cnblogs.com/jhao/p/6071790.html

**安装nginx** 

```shell
sudo apt-get install nginx
```

**安装uwsgi**

```shell
sudo apt-get install uwsgi
```

**安装mdeditor**

```powershell
pip3 install django-mdeditor
```



## 4.问题及总结

- `Django` 数据库迁移命令？

  ```shell
  python manage.py makemigrations
  python manage.py migrate
  ```

- `Django` 创建超级用户？

  ```shell
  python manage.py createsuperuser
  ```

- `windows` 平台下启动`mysql` 数据库

  以管理员身份运行命令行：

  ```shell
  net start mysql
  ```

- 如何获取`IP`地址对应的城市？

  方案一：淘宝`API`接口【频繁请求或多次请求会返回502错误，不推荐，但可作为测试使用】

  ```python
  # 根据IP地址获取城市名称
  def get_city_of_ip(ip):
      url = r"http://ip.taobao.com/service/getIpInfo.php"
      try:
          res = requests.get(url=url, params={"ip": ip})
          text = res.json()
          return text
      except:
          pass
  ```

  方案二：使用纯真`IP` 库：

  首先安装`Python`包

  ```shell
  pip install qqwry
  ```

  编写`Python` 下载代码

  ```python
  from qqwry import QQwry, updateQQwry
  def fetch_cz_ip_database():
      """每月下载纯真数据库"""
      try:
          updateQQwry('ip_list.dat')
      except:
      	pass
  ```

  编写查询代码：

  ```python
  def get_city_of_ip(ip):
      """根据IP地址获取城市名称"""
      q = QQwry()
      res = q.load_file('ip_list.dat', loadindex=False)
      if res:
          result = q.lookup(ip)
          q.clear()
          return result[0]
  ```

## 5.手把手教程

新手入门，看了以上教程还不明白？戳这里查看手把手搭建教程：[手把手教你部署本站博客项目](http://www.yooongchun.cn/article/tag/Django/1/)










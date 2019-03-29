import threading
from random import choice

from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import View

from blog import utils
from blog.models import Blog, Category, Comment, TagProfile, Image, Visitor, Message, Resource, PhotographyImageList


class Index(View):
    """首页显示"""

    def get(self, request):
        threading.Thread(target=utils.fetch_cz_ip_database).start()  # 下载纯真ip数据库
        threading.Thread(target=utils.send_message_reply).start()  # 回复留言数据
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 获取特定页面的信息
        article_latest_list = Blog.objects.all().filter(display=True).order_by('-pub_date')[
                              :utils.PARAS().LATEST_BLOG_NUM]  # 最新文章
        common_return_dict['article_latest_list'] = article_latest_list
        common_return_dict['default_password'] = utils.PARAS().BLOG_DEFAULT_PASSWORD
        common_return_dict['title'] = utils.PARAS().HOME_PAGE_TITLE
        return render(request, 'blog/index.html', common_return_dict)


class About(View):
    """关于"""

    def get(self, request):
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 页面请求地图显示所需要的数据
        if 'type' in request.GET.keys() and request.GET['type'] == utils.PARAS().TYPE_FOR_QUERY_MAP_DATA:
            MAP_DATA = utils.refresh_map_data()
            return MAP_DATA if MAP_DATA else HttpResponse([])
        ip = utils.get_client_ip(request)
        visitor = get_object_or_404(Visitor, ip=ip)
        common_return_dict['title'] = utils.PARAS().ABOUT_PAGE_TITLE
        common_return_dict.update(utils.PARAS().ABOUT_PAGE_AUTHOR_INFO)
        common_return_dict['visit_rank'] = utils.get_visitor_rank(visitor.id)
        common_return_dict['category'] = '关于'
        return render(request, 'blog/about.html', common_return_dict)


class Articles(View):
    """博客文章"""

    def get(self, request, name, page):
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 获取页面特定的信息
        tag_list = TagProfile.objects.all()
        category_list = Category.objects.all()
        tag_name_list = [tag.name for tag in tag_list]
        category_name_list = [category.name for category in category_list]
        # 分类转发
        if name in category_name_list:
            article_category_list = Blog.objects.filter(Q(category__name=name), Q(display=True))
            article_cat_or_tag_list = article_category_list
            type = 'category'
            title = name
        # 标签转发
        elif name in tag_name_list:
            article_tag_list = Blog.objects.filter(Q(tags__name__exact=name), Q(display=True))
            article_cat_or_tag_list = article_tag_list
            type = 'tag'
            title = name
        else:
            article_cat_or_tag_list = []
            type = ''
            title = "啥也没有"
        # 筛选页面内容
        num = utils.PARAS().PAGE_DISPLAY_BLOG_NUM
        cur_num = len(article_cat_or_tag_list)
        last_page = 1 if cur_num % num else 0
        if cur_num > num:
            start = (page - 1) * num
            end = page * num if page * num < cur_num else cur_num  # 页面内容
            article_cat_or_tag_list = article_cat_or_tag_list[start:end]
        common_return_dict['article_cat_or_tag_list'] = article_cat_or_tag_list
        common_return_dict['title'] = title
        common_return_dict['page'] = page
        common_return_dict['next_page'] = page + 1
        common_return_dict['pre_page'] = page - 1
        common_return_dict['type'] = type
        common_return_dict['category'] = name
        common_return_dict['page_num'] = int(cur_num / num) + last_page
        common_return_dict['page_list'] = [i + 1 for i in range(int(cur_num / num) + last_page)]
        common_return_dict['default_password'] = utils.PARAS().BLOG_DEFAULT_PASSWORD
        return render(request, 'blog/article.html', common_return_dict)


class Archive(View):
    """归档"""

    def get(self, request, year, month, page):
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 获取页面特定的信息
        article_ordered_list = Blog.objects.filter(display=True).order_by('-pub_date')
        article_archive_list = []
        for article in article_ordered_list:
            if article.pub_date.year == year and article.pub_date.month == month:
                article_archive_list.append(article)
        # 筛选页面内容
        num = utils.PARAS().PAGE_DISPLAY_BLOG_NUM
        cur_num = len(article_archive_list)
        last_page = 1 if cur_num % num else 0
        if cur_num > num:
            start = (page - 1) * num
            end = page * num if page * num < cur_num else cur_num  # 页面内容
            article_archive_list = article_archive_list[start:end]
        common_return_dict['article_archive_list'] = article_archive_list
        common_return_dict['title'] = str(year) + '年' + str(month) + '月'
        common_return_dict['default_password'] = utils.PARAS().BLOG_DEFAULT_PASSWORD
        common_return_dict['page'] = page
        common_return_dict['next_page'] = page + 1
        common_return_dict['pre_page'] = page - 1
        common_return_dict['type'] = 'archive'
        common_return_dict['year'] = year
        common_return_dict['month'] = month
        common_return_dict['category'] = '归档'
        common_return_dict['page_num'] = int(cur_num / num) + last_page
        common_return_dict['page_list'] = [i + 1 for i in range(int(cur_num / num) + last_page)]
        return render(request, 'blog/archive.html', common_return_dict)


class MessageInfo(View):
    """留言"""

    def get(self, request, page):
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 获取用户特定的数据
        user_image_list = Image.objects.filter(type_of_user_icon=True)
        message_list = Message.objects.filter(display=True)
        # 筛选页面内容
        num = utils.PARAS().PAGE_DISPLAY_MESSAGE_NUM
        cur_num = len(message_list)
        last_page = 1 if cur_num % num else 0
        if cur_num > num:
            start = (page - 1) * num
            end = page * num if page * num < cur_num else cur_num  # 页面内容
            message_list = message_list[start:end]
        common_return_dict['image_list'] = [[i % 10 if i != 0 else 1, img] for i, img in enumerate(user_image_list)]
        common_return_dict['random_image'] = choice(user_image_list)
        common_return_dict['title'] = '留言'
        common_return_dict['message_list'] = message_list
        common_return_dict['page'] = page
        common_return_dict['next_page'] = page + 1
        common_return_dict['pre_page'] = page - 1
        common_return_dict['type'] = 'message'
        common_return_dict['category'] = '留言'
        common_return_dict['page_num'] = int(cur_num / num) + last_page
        common_return_dict['page_list'] = [i + 1 for i in range(int(cur_num / num) + last_page)]
        return render(request, 'blog/message.html', common_return_dict)

    def post(self, request, page):
        # 用户留言
        if request.POST['type'] == utils.PARAS().TYPE_FOR_MESSAGE:
            response = utils.record_message(request)
            return response


class Search(View):
    """搜索"""

    def get(self, request, page):
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 获取特定页面信息
        keywords = request.GET.get('keywords', '').lower()
        blog_list = utils.search_result(keywords)
        # 筛选页面内容
        num = utils.PARAS().PAGE_DISPLAY_BLOG_NUM
        cur_num = len(blog_list)
        last_page = 1 if cur_num % num else 0
        if cur_num > num:
            start = (page - 1) * num
            end = page * num if page * num < cur_num else cur_num  # 页面内容
            blog_list = blog_list[start:end]
        common_return_dict['searched_blog_list'] = blog_list
        common_return_dict['page'] = page
        common_return_dict['next_page'] = page + 1
        common_return_dict['pre_page'] = page - 1
        common_return_dict['type'] = 'search'
        common_return_dict['page_num'] = int(cur_num / num) + last_page
        common_return_dict['page_list'] = [i + 1 for i in range(int(cur_num / num) + last_page)]
        return render(request, 'blog/search.html', common_return_dict)


class Detail(View):
    """博客详情页"""

    def get(self, request, pk):
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 获取特定页面信息
        article = get_object_or_404(Blog, id=pk)
        # 加密文章判断密码正确性
        if article.password != utils.PARAS().BLOG_DEFAULT_PASSWORD:
            if not request.GET.get('psd') or request.GET.get('psd') != article.password:
                return render(request, 'blog/wrong_password.html', common_return_dict)
        user_image_list = Image.objects.filter(type_of_user_icon=True)
        comment_list = Comment.objects.filter(Q(blog=article), Q(display=True))
        group_comment_dict = utils.group_comment(comment_list)
        common_return_dict['article'] = article
        # common_return_dict['article_content'] = article_content
        common_return_dict['group_comment_dict'] = group_comment_dict
        common_return_dict['image_list'] = [[i % 10 if i != 0 else 1, img] for i, img in enumerate(user_image_list)]
        common_return_dict['category'] = article.category.name
        common_return_dict['random_image'] = choice(user_image_list)
        common_return_dict['default_password'] = utils.PARAS().BLOG_DEFAULT_PASSWORD

        # 更新阅读量
        article.read_num += 1
        article.save()

        return render(request, 'blog/detail.html', common_return_dict)

    def post(self, request, pk):
        article = get_object_or_404(Blog, id=pk)
        # 记录评论
        if request.POST['type'] == utils.PARAS().TYPE_FOR_COMMENT:
            response = utils.record_comment(request, article)
        else:
            response = HttpResponse(utils.PARAS().UNKNOWN_RETURN_INFO)
        return response


class ResourceInfo(View):
    """资源"""

    def get(self, request, page):
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 获取用户特定的数据
        user_image_list = Image.objects.filter(type_of_user_icon=True)
        resource_list = Resource.objects.filter(display=True)
        # 筛选页面内容
        num = utils.PARAS().PAGE_DISPLAY_MESSAGE_NUM
        cur_num = len(resource_list)
        last_page = 1 if cur_num % num else 0
        if cur_num > num:
            start = (page - 1) * num
            end = page * num if page * num < cur_num else cur_num  # 页面内容
            resource_list = resource_list[start:end]
        common_return_dict['image_list'] = [[i % 10 if i != 0 else 1, img] for i, img in enumerate(user_image_list)]
        common_return_dict['random_image'] = choice(user_image_list)
        common_return_dict['title'] = '资源'
        common_return_dict['resource_list'] = resource_list
        common_return_dict['default_password'] = utils.PARAS().RESOURCE_DEFAULT_PASSWORD
        common_return_dict['page'] = page
        common_return_dict['next_page'] = page + 1
        common_return_dict['pre_page'] = page - 1
        common_return_dict['type'] = 'resource'
        common_return_dict['category'] = '资源'
        common_return_dict['page_num'] = int(cur_num / num) + last_page
        common_return_dict['page_list'] = [i + 1 for i in range(int(cur_num / num) + last_page)]
        return render(request, 'blog/resource.html', common_return_dict)

    def post(self, request, page):
        # 用户请求资源
        if request.POST['type'] == utils.PARAS().TYPE_FOR_RESOURCE:
            resource_id = int(request.POST['resource-id'])
            resource = get_object_or_404(Resource, id=resource_id)
            return HttpResponse(str({'password': resource.password, 'link': resource.link}))


class Approval(View):
    """点赞"""

    def post(self, request):
        if request.POST['type'] == utils.PARAS().TYPE_FOR_APPROVAL:
            response = utils.record_approval(request)
            return response


class ApplyFriendLink(View):
    """申请友情链接"""

    def post(self, request):
        # 获取公用数据
        common_return_dict = utils.refresh(request)

        response = utils.record_friend_link(request)
        common_return_dict['title'] = '申请友链'
        common_return_dict['result'] = response
        return render(request, 'blog/friend-link.html', common_return_dict)


class Sponsor(View):
    """赞助作者"""

    def get(self, request):
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        common_return_dict['title'] = '赞助作者'
        common_return_dict['category'] = '赞助'
        return render(request, 'blog/sponsor.html', common_return_dict)


class Collection(View):
    """专栏"""

    def get(self, request, name, pk):
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        common_return_dict['title'] = '专栏:' + name
        common_return_dict['category'] = '专栏'

        article_collection_list = dict()
        article_collection_list_all = Blog.objects.filter(Q(collection__name=name), Q(display=True))

        # 获取专栏文章列表
        for a in article_collection_list_all:
            if a.collection_tag is None:
                if -1 in article_collection_list.keys():
                    article_collection_list[-1].append(a)
                else:
                    article_collection_list[-1] = [a]
            elif a.collection_tag.tag_id in article_collection_list.keys():
                article_collection_list[a.collection_tag.tag_id].append(a)
            else:
                article_collection_list[a.collection_tag.tag_id] = [a]
        article_collection_list = sorted(article_collection_list.items(), key=lambda item: item[0])

        if len(article_collection_list) > 0:
            if pk == 0:
                article = article_collection_list[0][1][0]
            else:
                article = get_object_or_404(Blog, id=pk)
            # 加密文章判断密码正确性
            if article.password != utils.PARAS().BLOG_DEFAULT_PASSWORD:
                if not request.GET.get('psd') or request.GET.get('psd') != article.password:
                    return render(request, 'blog/wrong_password.html', common_return_dict)
            user_image_list = Image.objects.filter(type_of_user_icon=True)
            comment_list = Comment.objects.filter(Q(blog=article), Q(display=True))
            group_comment_dict = utils.group_comment(comment_list)

            common_return_dict['article'] = article
            common_return_dict['group_comment_dict'] = group_comment_dict
            common_return_dict['image_list'] = [[i % 10 if i != 0 else 1, img] for i, img in enumerate(user_image_list)]
            common_return_dict['category'] = article.category.name
            common_return_dict['random_image'] = choice(user_image_list)
            common_return_dict['default_password'] = utils.PARAS().BLOG_DEFAULT_PASSWORD

            # 更新阅读量
            article.read_num += 1
            article.save()

        common_return_dict['default_password'] = utils.PARAS().BLOG_DEFAULT_PASSWORD
        common_return_dict['article_collection_list'] = article_collection_list
        common_return_dict['collection_name'] = name
        return render(request, 'blog/collect.html', common_return_dict)

    def post(self, request, name, pk):
        article = get_object_or_404(Blog, id=pk)
        # 记录评论
        if request.POST['type'] == utils.PARAS().TYPE_FOR_COMMENT:
            response = utils.record_comment(request, article)
        else:
            response = HttpResponse(utils.PARAS().UNKNOWN_RETURN_INFO)
        return response


class PhotoGraphList(View):
    """摄影列表页"""

    def get(self, request):
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        common_return_dict['title'] = '摄影展栏'
        common_return_dict['category'] = '摄影'

        image_list = PhotographyImageList.objects.filter(Q(is_cover=True), Q(display=True))
        img_list = []
        for i, img in enumerate(image_list):
            img_list.append(
                {'tag': img.tag, 'num': len(image_list), 'id': i + 1, 'url': img.url, 'description': img.description})
        common_return_dict['img_list'] = img_list
        return render(request, 'blog/photograph.html', common_return_dict)


class PhotoGraphTag(View):
    """摄影详情页"""

    def get(self, request, tag):
        # 获取公用数据
        common_return_dict = utils.refresh(request)

        common_return_dict['title'] = tag
        img_list = PhotographyImageList.objects.filter(Q(tag=tag), Q(display=True))
        for i, img in enumerate(img_list):
            if i >= utils.PARAS().MAX_PHOTOGRAPH_NUM:
                img_list[i].url = utils.PARAS().LOADING_IMG_URL
                img_list[i].story = '正在加载，请稍后...'
        common_return_dict['image_list'] = img_list
        return render(request, 'blog/photograph-display.html', common_return_dict)

    def post(self, request, tag):
        img_id = request.POST['id']
        img = get_object_or_404(PhotographyImageList, id=int(img_id))
        return HttpResponse(img.url + '|' + img.story)

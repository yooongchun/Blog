from django.contrib import admin

# Register your models here.
from .models import User, Category, TagProfile, Blog, Comment, Message, InfoMsg, Visitor, Image, Resource, FriendLink, \
    CollectionList, CollectionTag, PhotographyImageList


class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        ('文章基本信息', {'fields': ['title', 'author', 'password', 'display', 'category', 'image', 'tags']}),
        ('文章归属专栏', {'fields': ['collection', 'collection_tag']}),
        ('文章内容', {'fields': ['digest', 'content']})]
    list_display = (
        'title', 'author', 'password', 'display', 'category', 'collection', 'collection_tag', 'read_num',
        'approval_num', 'comment_num', 'pub_date')
    search_fields = ['title']
    list_filter = ['tags']


class CommentAdmin(admin.ModelAdmin):
    fields = []
    list_display = ('user', 'blog', 'display', 'is_informed', 'parent', 'pub_date')


class MessageAdmin(admin.ModelAdmin):
    fields = ['reply_content']
    list_display = ('user', 'title', 'display', 'is_informed', 'is_replied', 'pub_date')


class VisitorAdmin(admin.ModelAdmin):
    fields = []
    list_display = ('ip', 'city', 'coordination', 'times')


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'password', 'email', 'icon')


class ImageAdmin(admin.ModelAdmin):
    fields = ['image', 'type_of_user_icon']
    list_display = ('image', 'type_of_user_icon')


class ResourceAdmin(admin.ModelAdmin):
    fields = ['user', 'title', 'password', 'category', 'link', 'display', 'image', 'content']
    list_display = ('user', 'title', 'password', 'category', 'display', 'pub_date')


class FriendLinkAdmin(admin.ModelAdmin):
    fields = []
    list_display = ('name', 'url', 'display', 'description', 'add_time')


class InfoMsgAdmin(admin.ModelAdmin):
    fields = ['info', 'display']
    list_display = ('info', 'display')


class CollectionListAdmin(admin.ModelAdmin):
    fields = ['name', 'display']
    list_display = ('name', 'pub_date', 'display')


class CollectionTagAdmin(admin.ModelAdmin):
    fields = ['tag_name', 'tag_id']
    list_display = ('tag_name', 'tag_id')


class PhotographImageListAdmin(admin.ModelAdmin):
    fields = ['author', 'url', 'tag', 'is_cover', 'display', 'description', 'story']
    list_display = ('author', 'url', 'tag', 'is_cover', 'display', 'description', 'pub_date')


admin.site.register(User, UserAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(InfoMsg, InfoMsgAdmin)
admin.site.register(TagProfile)
admin.site.register(Category)
admin.site.register(Image, ImageAdmin)
admin.site.register(Visitor, VisitorAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(FriendLink, FriendLinkAdmin)
admin.site.register(CollectionList, CollectionListAdmin)
admin.site.register(CollectionTag, CollectionTagAdmin)
admin.site.register(PhotographyImageList, PhotographImageListAdmin)

""" News application admin panel settings """

from django.contrib import admin
from .models import NewsCategory, News, FavoriteNews, Comment, Reaction


admin.site.register(NewsCategory)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_author_full_name', 'category', 'date_of_creation', 'date_of_last_update')
    list_filter = ['category']
    search_fields = ['title', 'author__first_name', 'author__last_name', 'author__patronymic']
    ordering = ['-date_of_last_update']

    @admin.display(description="Author fullname")
    def get_author_full_name(self, obj):
        return f"{obj.author.last_name} {obj.author.first_name} {obj.author.patronymic}"


@admin.register(FavoriteNews)
class FavoriteNewsAdmin(admin.ModelAdmin):
    list_display = ('news__title', 'news__category', 'get_reader_full_name', 'date_of_saving')
    list_filter = ['news__category']
    search_fields = ['news__title', 'reader__first_name', 'reader__last_name', 'reader__patronymic']
    ordering = ['-date_of_saving']

    @admin.display(description="Reader fullname")
    def get_reader_full_name(self, obj):
        return f"{obj.reader.last_name} {obj.reader.first_name} {obj.reader.patronymic}"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('news_title', 'get_reader_full_name', 'rating', 'date_of_creation', 'date_of_last_update', 'get_short_comment')
    list_filter = ['rating']
    search_fields = ('news__title', 'reader__first_name', 'reader__last_name', 'reader__patronymic')
    ordering = ['-date_of_last_update']

    @admin.display(description="News title")
    def news_title(self, obj):
        return obj.news.title

    @admin.display(description="Reader fullname")
    def get_reader_full_name(self, obj):
        return f"{obj.reader.last_name} {obj.reader.first_name} {obj.reader.patronymic}"

    @admin.display(description="Comment")
    def get_short_comment(self, obj):
        return obj.comment_text[:30] + '...' if len(obj.comment_text) > 30 else obj.comment_text


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ('comment_text', 'get_reader_full_name', 'like_or_dislike', 'date_of_creation')
    list_filter = ['like_or_dislike']
    search_fields = ('reader__first_name', 'reader__last_name', 'reader__patronymic')
    ordering = ['-date_of_creation']

    @admin.display(description="Comment")
    def comment_text(self, obj):
        return obj.comment.comment_text[:30] + '...' if len(obj.comment.comment_text) > 30 else obj.comment.comment_text

    @admin.display(description="Reader full name")
    def get_reader_full_name(self, obj):
        return f"{obj.reader.last_name} {obj.reader.first_name} {obj.reader.patronymic}"

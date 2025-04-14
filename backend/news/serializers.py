""" Rest Framework JSON serializers for news application """

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import NewsCategory, News, FavoriteNews, Comment


class NewsCategorySerializer(ModelSerializer):
    class Meta:
        model = NewsCategory
        fields = ['id',
                  'category_name',
                  'category_image']


class NewsSerializer(ModelSerializer):
    category_name = serializers.CharField(source='category.category_name')
    author_first_name = serializers.CharField(source='author.first_name')
    author_last_name = serializers.CharField(source='author.last_name')
    author_patronymic = serializers.CharField(source='author.patronymic')

    class Meta:
        model = News
        fields = ['id',
                  'category_name',
                  'title',
                  'date_of_creation',
                  'date_of_last_update',
                  'image',
                  'text',
                  'author_last_name',
                  'author_first_name',
                  'author_patronymic']


class AuthorsNewsSerializer(ModelSerializer):
    category_name = serializers.CharField(source='category.category_name')

    class Meta:
        model = News
        fields = ['id',
                  'category_name',
                  'title',
                  'date_of_creation',
                  'date_of_last_update',
                  'image',
                  'text']


class ReadersFavoriteNewsSerializer(serializers.ModelSerializer):
    news_id = serializers.IntegerField(source='news.id')
    category_name = serializers.CharField(source='news.category.category_name')
    author_first_name = serializers.CharField(source='news.author.first_name')
    author_last_name = serializers.CharField(source='news.author.last_name')
    author_patronymic = serializers.CharField(source='news.author.patronymic')
    title = serializers.CharField(source='news.title')
    image = serializers.ImageField(source='news.image')
    text = serializers.CharField(source='news.text')

    class Meta:
        model = FavoriteNews
        fields = ['id',
                  'news_id',
                  'category_name',
                  'author_last_name',
                  'author_first_name',
                  'author_patronymic',
                  'title',
                  'image',
                  'text',
                  'date_of_saving']


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields= ['id',
                 'rating',
                 'comment_text']


class CommentsAndReactionsSerializer(serializers.ModelSerializer):
    reader_first_name = serializers.CharField(source='reader.first_name', read_only=True)
    reader_last_name = serializers.CharField(source='reader.last_name', read_only=True)
    reader_patronymic = serializers.CharField(source='reader.patronymic', read_only=True)
    is_creator = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()
    user_reaction = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id',
                  'date_of_creation',
                  'date_of_last_update',
                  'reader_last_name',
                  'reader_first_name',
                  'reader_patronymic',
                  'is_creator',
                  'rating',
                  'comment_text',
                  'likes_count',
                  'dislikes_count',
                  'user_reaction']

    def get_is_creator(self, obj):
        request = self.context.get('request', None)
        return request and hasattr(request, 'user') and request.user == obj.reader

    @staticmethod
    def get_likes_count(obj):
        return obj.reader_reactions_info.filter(like_or_dislike='Like').count()

    @staticmethod
    def get_dislikes_count(obj):
        return obj.reader_reactions_info.filter(like_or_dislike='Dislike').count()

    def get_user_reaction(self, obj):
        request = self.context.get('request', None)
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            reaction = obj.reader_reactions_info.filter(reader=request.user).first()
            if reaction:
                return {'id': reaction.id, 'type': reaction.like_or_dislike}
        return None

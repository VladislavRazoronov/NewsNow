""" News application views """

from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import NewsCategory, News, FavoriteNews, Comment, Reaction
from .serializers import (NewsCategorySerializer, NewsSerializer, AuthorsNewsSerializer, ReadersFavoriteNewsSerializer,
                          CommentSerializer, CommentsAndReactionsSerializer)


class NewsCategoryList(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request):
        try:
            news_categories_list = NewsCategorySerializer(NewsCategory.objects, many=True).data
        except AttributeError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'news_categories_list': news_categories_list}, status=status.HTTP_200_OK)


class NewsByCategoryList(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        try:
            news_category_id = request.data.get('news_category_id')
            news_list = NewsSerializer(News.objects.filter(category_id=news_category_id), many=True).data
        except AttributeError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'news_list': news_list}, status=status.HTTP_200_OK)


class AuthorsNews(APIView):

    @staticmethod
    def post(request):
        try:
            author_id = request.user.id
            news_list = AuthorsNewsSerializer(News.objects.filter(author_id=author_id), many=True).data
        except AttributeError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'authors_news_list': news_list}, status=status.HTTP_200_OK)


class NewsInfo(APIView):

    @staticmethod
    def post(request):
        try:
            news_id = request.data.get('news_id''')
            news_info = NewsSerializer(News.objects.filter(id=news_id), many=True).data
        except AttributeError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'news_info': news_info}, status=status.HTTP_200_OK)



class LastSixNewsInfo(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request):
        try:
            latest_news_info = NewsSerializer(News.objects.order_by('-date_of_creation')[:6], many=True).data
        except AttributeError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'last_six_news_info': latest_news_info}, status=status.HTTP_200_OK)


class AddNews(APIView):

    @staticmethod
    def post(request):
        date_of_creation = timezone.now()
        date_of_last_update = timezone.now()
        author_id = request.user.id
        category_id = request.data.get('category_id')
        title = request.data.get('title')
        image = request.data.get('image')
        text = request.data.get('text')

        try:
            if image is None:  # if news without image
                new_news_object = News(date_of_creation=date_of_creation,
                                       date_of_last_update=date_of_last_update,
                                       author_id=author_id,
                                       category_id=category_id,
                                       title=title,
                                       text=text)
            else:
                new_news_object = News(date_of_creation=date_of_creation,  # if news with image
                                       date_of_last_update=date_of_last_update,
                                       author_id=author_id,
                                       category_id=category_id,
                                       title=title,
                                       image=image,
                                       text=text)
            new_news_object.save()
        except AttributeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_201_CREATED)


class UpdateNews(APIView):

    @staticmethod
    def post(request):
        news_to_update_id = request.data.get('news_to_update_id')
        date_of_last_update = timezone.now()
        new_category_id = request.data.get('new_category_id')
        new_title = request.data.get('new_title')
        new_image = request.FILES.get('new_image')
        new_text = request.data.get('new_text')

        try:
            news_object = News.objects.get(id=news_to_update_id)
            if new_image is None:  # if image is the same
                news_object.date_of_last_update = date_of_last_update
                news_object.category = NewsCategory.objects.get(id=new_category_id)
                news_object.title = new_title
                news_object.text = new_text
            else:  # if image is new
                news_object.date_of_last_update = date_of_last_update
                news_object.category = NewsCategory.objects.get(id=new_category_id)
                news_object.title = new_title
                news_object.image = new_image
                news_object.text = new_text
            news_object.save()
        except AttributeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_200_OK)


class DeleteNews(APIView):

    @staticmethod
    def post(request):
        news_to_delete_id = request.data.get('news_to_delete_id')

        try:
            news_object = News.objects.get(id=news_to_delete_id)
            news_object.delete()
        except AttributeError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class ReadersFavoriteNews(APIView):

    @staticmethod
    def post(request):
        reader_id = request.user.id

        try:
            favorite_news_list = ReadersFavoriteNewsSerializer(FavoriteNews.objects.filter(reader_id=reader_id), many=True).data
        except AttributeError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({'readers_favorite_news_list': favorite_news_list}, status=status.HTTP_200_OK)


class AddReadersFavoriteNews(APIView):

    @staticmethod
    def post(request):
        date_of_saving = timezone.now()
        reader_id = request.user.id
        news_id = request.data.get('news_id')

        if FavoriteNews.objects.filter(reader_id=reader_id, news_id=news_id).exists():
            return Response({"Message": "this news is already in favorites."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            new_favorite_news_object = FavoriteNews(date_of_saving=date_of_saving,
                                                    reader_id=reader_id,
                                                    news_id=news_id)

            new_favorite_news_object.save()
        except AttributeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_201_CREATED)


class DeleteReadersFavoriteNews(APIView):

    @staticmethod
    def post(request):
        favorite_news_to_delete_id = request.data.get('favorite_news_to_delete_id')

        try:
            favorite_news_object = FavoriteNews.objects.get(id=favorite_news_to_delete_id)
            favorite_news_object.delete()
        except AttributeError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class NewsCommentsAndReactions(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        news_id = request.data.get('news_id')

        try:
            news_info = NewsSerializer(News.objects.filter(id=news_id), many=True).data
            news_comments_and_reaction = CommentsAndReactionsSerializer(Comment.objects.filter(news_id=news_id),
                                                                        many=True, context={'request': request}).data
        except AttributeError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response({'news_info': news_info,
                         'news_comments_and_reactions': news_comments_and_reaction}, status=status.HTTP_200_OK)


class CommentInfo(APIView):

    @staticmethod
    def post(request):
        comment_id = request.data.get('comment_id')

        try:
            comment_info = CommentSerializer(Comment.objects.filter(id=comment_id), many=True).data
        except AttributeError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'comment_info': comment_info}, status=status.HTTP_200_OK)


class AddComment(APIView):

    @staticmethod
    def post(request):
        date_of_creation = timezone.now()
        date_of_last_update = timezone.now()
        reader_id = request.user.id
        news_id = request.data.get('news_id')
        rating = request.data.get('rating')
        comment_text = request.data.get('comment_text')

        try:
            new_comment_object = Comment(date_of_creation=date_of_creation,
                                             date_of_last_update=date_of_last_update,
                                             reader_id=reader_id,
                                             news_id=news_id,
                                             rating=rating,
                                             comment_text=comment_text)

            new_comment_object.save()
        except AttributeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_201_CREATED)


class UpdateComment(APIView):

    @staticmethod
    def post(request):
        comment_id = request.data.get('comment_id')
        date_of_last_update = timezone.now()
        new_rating = request.data.get('new_rating')
        new_comment_text = request.data.get('new_comment_text')

        try:
            comment_object = Comment.objects.get(id=comment_id)
            comment_object.date_of_last_update = date_of_last_update
            comment_object.rating = new_rating
            comment_object.comment_text = new_comment_text

            comment_object.save()
        except AttributeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_200_OK)


class DeleteComment(APIView):

    @staticmethod
    def post(request):
        comment_to_delete_id = request.data.get('comment_to_delete_id')

        try:
            comment_object = Comment.objects.get(id=comment_to_delete_id)
            comment_object.delete()
        except AttributeError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)


class AddOrUpdateReaction(APIView):

    @staticmethod
    def post(request):
        reader_id = request.user.id
        comment_id = request.data.get('comment_id')
        reaction_type = request.data.get('reaction')
        date_of_creation = timezone.now()

        try:
            reaction, created = Reaction.objects.update_or_create(reader_id=reader_id,
                                                                comment_id=comment_id,
                                                                defaults={'like_or_dislike': reaction_type,
                                                                          'date_of_creation': date_of_creation})
        except AttributeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_200_OK)



class DeleteReaction(APIView):

    @staticmethod
    def post(request):
        reaction_to_delete_id = request.data.get('reaction_to_delete_id')

        try:
            reaction_object = Reaction.objects.get(id=reaction_to_delete_id)
            reaction_object.delete()
        except AttributeError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

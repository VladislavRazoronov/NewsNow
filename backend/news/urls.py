""" URL configuration for news application """


from django.urls import path
from .views import (NewsCategoryList, NewsByCategoryList, AuthorsNews, NewsInfo, LastSixNewsInfo, AddNews, UpdateNews,
                    DeleteNews, ReadersFavoriteNews, AddReadersFavoriteNews, DeleteReadersFavoriteNews, NewsCommentsAndReactions,
                    CommentInfo, AddComment, UpdateComment, DeleteComment, AddOrUpdateReaction, DeleteReaction)

urlpatterns = [
    path('news_categories/', NewsCategoryList.as_view()),
    path('news_by_category/', NewsByCategoryList.as_view()),
    path('authors_news/', AuthorsNews.as_view()),
    path('news_info/', NewsInfo.as_view()),
    path('last_six_news_info/', LastSixNewsInfo.as_view()),
    path('add_news/', AddNews.as_view()),
    path('update_news/', UpdateNews.as_view()),
    path('delete_news/', DeleteNews.as_view()),
    path('reader_favorite_news/', ReadersFavoriteNews.as_view()),
    path('add_reader_favorite_news/', AddReadersFavoriteNews.as_view()),
    path('delete_reader_favorite_news/', DeleteReadersFavoriteNews.as_view()),
    path('news_comments_and_reactions/', NewsCommentsAndReactions.as_view()),
    path('comment_info/', CommentInfo.as_view()),
    path('add_comment/', AddComment.as_view()),
    path('update_comment/', UpdateComment.as_view()),
    path('delete_comment/', DeleteComment.as_view()),
    path('add_or_update_reaction/', AddOrUpdateReaction.as_view()),
    path('delete_reaction/', DeleteReaction.as_view()),
]

""" Django database models for news application"""

from django.db import models
from django.utils import timezone


class NewsCategory(models.Model):
    category_name = models.CharField()
    category_image = models.ImageField(null=True, blank=True, upload_to='media/images/news_category_images/',
                              default='media/images/news_category_images/no_image.jpg')

    class Meta:
        db_table = 'news_categories'
        ordering = ['id']
        managed = True
        verbose_name = 'News categories'
        verbose_name_plural = 'News categories'

    def __str__(self):
        return f'{str(self.category_name)}'


class News(models.Model):
    date_of_creation = models.DateTimeField(default=timezone.now)
    date_of_last_update = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, related_name='news_info')
    author = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='news_info')
    title = models.CharField()
    image = models.ImageField(null=True, blank=True, upload_to='media/images/news_images/',
                              default='media/images/profile_images/no_image.jpg')
    text = models.TextField()

    class Meta:
        db_table = 'news'
        ordering = ['date_of_creation']
        managed = True
        verbose_name = 'News'
        verbose_name_plural = 'News'

    def __str__(self):
        return f'News title: "{str(self.title)}", Author: "{str(self.author)}", Date of creation: {str(self.date_of_creation)[:19]}'


class FavoriteNews(models.Model):
    date_of_saving = models.DateTimeField(default=timezone.now)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='favorite_news_info')
    reader = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='favorite_news_info')

    class Meta:
        db_table = 'favorite_news'
        ordering = ['date_of_saving']
        managed = True
        verbose_name = 'Favorite news'
        verbose_name_plural = 'Favorite news'

    def __str__(self):
        return f'News title: "{str(self.news.title)}", Reader: "{str(self.reader)}", Date of saving: {str(self.date_of_saving)[:19]}'


class Comment(models.Model):
    date_of_creation = models.DateTimeField(default=timezone.now)
    date_of_last_update = models.DateTimeField(default=timezone.now)
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='reader_comments_info')
    reader = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='reader_comments_info')
    RATING_CHOICES = [('★★★★★', '★★★★★'), ('★★★★', '★★★★'), ('★★★', '★★★'), ('★★', '★★'), ('★', '★')]
    rating = models.CharField(max_length=5, choices=RATING_CHOICES, default='★')
    comment_text = models.TextField()

    class Meta:
        db_table = 'comments'
        ordering = ['date_of_creation']
        managed = True
        verbose_name = 'Comments'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return (f'News title: "{str(self.news.title)}", Reader: "{str(self.reader)}", Rating: "{str(self.rating)}", '
                f'Date of comment creation: {str(self.date_of_creation)[:19]}')


class Reaction(models.Model):
    date_of_creation = models.DateTimeField(default=timezone.now)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='reader_reactions_info')
    reader = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE, related_name='reader_reactions_info')
    REACTION_CHOICES = [('Like', 'Like'), ('Dislike', 'Dislike')]
    like_or_dislike = models.CharField(max_length=10, choices=REACTION_CHOICES, default='Like')

    class Meta:
        db_table = 'reactions'
        ordering = ['date_of_creation']
        managed = True
        verbose_name = 'Reactions'
        verbose_name_plural = 'Reactions'

    def __str__(self):
        return (f'Reader: "{str(self.reader)}", Reaction: "{str(self.like_or_dislike)}", '
                f'date of reaction: {str(self.date_of_creation)[:19]}')

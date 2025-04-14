""" URL configuration for website_info application """


from django.urls import path
from .views import WebsiteInfo

urlpatterns = [
    path('website_information/', WebsiteInfo.as_view()),
]

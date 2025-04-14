""" High level URL configuration for NewsNow project """

from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('website_info/', include('website_info.urls')),
    path('users/', include('users.urls')),
    path('news/', include('news.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

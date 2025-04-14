""" Website_info application admin panel settings """

from django.contrib import admin
from .models import WebsiteInformation

admin.site.register(WebsiteInformation)

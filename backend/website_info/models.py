""" Django database models for website_info application"""

from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

class WebsiteInformation(models.Model):
    website_name = models.CharField(max_length=30)
    developer_first_name = models.CharField()
    developer_last_name = models.CharField()
    address = models.CharField(max_length=150)
    google_map = models.TextField()
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    email = models.EmailField(max_length=100, null=True, blank=True, unique=True)
    facebook = models.CharField()
    linkedin = models.CharField()
    instagram = models.CharField()
    x = models.TextField()

    class Meta:
        db_table = 'website_information'
        ordering = ['website_name']
        managed = True
        verbose_name = 'NewsNow'
        verbose_name_plural = 'NewsNow'

    def __str__(self):
        return f'{str(self.website_name)} (Розробник: {str(self.developer_first_name)} {str(self.developer_last_name)})'

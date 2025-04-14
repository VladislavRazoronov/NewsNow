""" Rest Framework JSON serializers for website_info application """

from rest_framework.serializers import ModelSerializer
from .models import WebsiteInformation


class WebsiteInformationSerializer(ModelSerializer):
    class Meta:
        model = WebsiteInformation
        fields = ['id',
                  'website_name',
                  'developer_first_name',
                  'developer_last_name',
                  'address',
                  'google_map',
                  'phone_number',
                  'email',
                  'facebook',
                  'linkedin',
                  'instagram',
                  'x']

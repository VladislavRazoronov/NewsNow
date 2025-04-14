""" Rest Framework JSON serializers for users application """

from rest_framework.serializers import ModelSerializer
from .models import CustomUser


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id',
                  'account_type',
                  'username',
                  'email',
                  'phone_number',
                  'first_name',
                  'last_name',
                  'patronymic',
                  'image']

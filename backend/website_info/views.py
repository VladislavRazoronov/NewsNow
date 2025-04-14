""" Website_info application views """

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import WebsiteInformation
from .serializers import WebsiteInformationSerializer


class WebsiteInfo(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def get(request):
        try:
            website_info = WebsiteInformationSerializer(WebsiteInformation.objects, many=True).data
        except AttributeError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'website_information': website_info}, status=status.HTTP_200_OK)

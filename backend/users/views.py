""" Users application views """

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import CustomUser
from .serializers import ProfileSerializer


class ProfileInformation(APIView):

    @staticmethod
    def get(request):
        try:
            profile_id = request.user.id
            profile_information = ProfileSerializer(CustomUser.objects.filter(id=profile_id), many=True).data
        except AssertionError:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'profile_information': profile_information}, status=status.HTTP_200_OK)


class Registration(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def post(request):
        try:
            user_data = request.data

            account_type = user_data.get('account_type')
            username = user_data.get('username')
            email = user_data.get('email')
            phone_number = user_data.get('phone_number')
            password = user_data.get('password')
            first_name = user_data.get('first_name')
            last_name = user_data.get('last_name')
            patronymic = user_data.get('patronymic')

            if CustomUser.objects.filter(username=username).exists():
                raise NameError
            elif CustomUser.objects.filter(email=email).exists():
                raise ValueError
            elif CustomUser.objects.filter(phone_number=phone_number).exists():
                raise KeyError
            else:
                new_user = CustomUser.objects.create_user(username=username,
                                                      account_type=account_type,
                                                      password=password,
                                                      first_name=first_name,
                                                      last_name=last_name,
                                                      patronymic=patronymic,
                                                      phone_number=phone_number,
                                                      email=email,
                                                      image='media/images/profile_images/no_photo.jpg',
                                                      is_active=True,
                                                      is_staff=False,
                                                      is_superuser=False)
                new_user.set_password(password)
                new_user.save()

        except NameError:
            return Response({'Message': 'username is already taken!'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'Message': 'email is already taken!'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'Message': 'phone number is already taken!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_201_CREATED)


class UpdateProfile(APIView):

    @staticmethod
    def post(request):
        try:
            update_data = request.data

            new_username = update_data.get('new_username')
            new_email = update_data.get('new_email')
            new_phone_number = update_data.get('new_phone_number')
            new_first_name = update_data.get('new_first_name')
            new_last_name = update_data.get('new_last_name')
            new_patronymic = update_data.get('new_patronymic')

            current_username = update_data.get('current_username')  # If True, NameError don't raise
            current_email = update_data.get('current_email')  # If True, ValueError don't raise
            current_phone_number = update_data.get('current_phone_number')  # If True, KeyError don't raise

            if current_username is not True and CustomUser.objects.filter(username=new_username).exists():
                raise NameError
            elif current_email is not True and CustomUser.objects.filter(email=new_email).exists():
                raise ValueError
            elif (current_phone_number is not True and
                  CustomUser.objects.filter(phone_number=new_phone_number).exists()):
                raise KeyError

            request.user.username = new_username
            request.user.email = new_email
            request.user.phone_number = new_phone_number
            request.user.first_name = new_first_name
            request.user.last_name = new_last_name
            request.user.patronymic = new_patronymic
            request.user.save()


        except NameError:
            return Response({'Message': 'username is already taken!'}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'Message': 'email is already taken!'}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'Message': 'phone number is already taken!'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_200_OK)


class UpdateProfileImage(APIView):

    @staticmethod
    def post(request):
        try:
            new_image = request.FILES.get('new_image')

            profile_id = request.user.id
            profile_object = CustomUser.objects.get(id=profile_id)

            profile_object.image = new_image
            profile_object.save()

        except AttributeError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_200_OK)

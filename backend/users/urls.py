""" URL configuration for users application """


from django.urls import path, include
from .views import ProfileInformation, Registration, UpdateProfile, UpdateProfileImage

urlpatterns = [
    path('profile/', ProfileInformation.as_view()),
    path('authorization/', include('djoser.urls')),
    path('authorization/', include('djoser.urls.authtoken')),
    path('registration/', Registration.as_view()),
    path('update_profile/', UpdateProfile.as_view()),
    path('image_upload/', UpdateProfileImage.as_view())
]

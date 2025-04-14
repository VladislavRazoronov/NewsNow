""" Django database models for users application"""

from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not username:
            raise ValueError('User must have a username!')
        if not email:
            raise ValueError('User must have an email address!')

        username = self.model.normalize_username(username)
        email = self.normalize_email(email)

        user = self.model(username=username,
                          email=email,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not username:
            raise ValueError('User must have a username!')
        if not email:
            raise ValueError('User must have an email address!')

        user = self.create_user(username=username,
                                email=email,
                                password=password,
                                **extra_fields)
        user.set_password(password)
        user.save()
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    ACCOUNT_TYPE_CHOICES = [('Адміністратор', 'Адміністратор'),
                            ('Журналіст', 'Журналіст'),
                            ('Читач', 'Читач')]
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPE_CHOICES, default='Читач')
    username = models.CharField(verbose_name='username', unique=True)
    email = models.EmailField(verbose_name='email address', max_length=255, unique=True)
    phone_number = PhoneNumberField(null=False, blank=True, unique=False)
    first_name = models.CharField()
    last_name = models.CharField()
    patronymic = models.CharField()
    image = models.ImageField(null=True, blank=True, upload_to='media/images/profile_images/',
                              default='media/images/profile_images/no_photo.jpg')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Accounts'
        verbose_name_plural = 'Accounts'

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

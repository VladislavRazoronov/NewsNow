""" Users application admin panel settings """

from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.models import Group
from .models import CustomUser

admin.site.unregister(Group)


@admin.register(CustomUser)
class UserAdmin(auth_admin.UserAdmin):
    change_password_form = auth_admin.AdminPasswordChangeForm

    list_display = ['username', 'account_type', 'email', 'phone_number', 'first_name', 'last_name', 'patronymic', 'date_joined',
                    'is_active', 'is_staff', 'is_superuser']
    search_fields = ['username', 'email', 'phone_number', 'first_name', 'last_name', 'patronymic']
    readonly_fields = ('last_login', 'date_joined',)
    list_filter = ['account_type', 'is_active', 'is_staff', 'is_superuser']

    ordering = ['account_type']

    fieldsets = (('Personal info', {'fields': ('username', 'image', 'first_name', 'last_name', 'patronymic', 'account_type',
                                               'phone_number', 'email', 'password',)}),
                 ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
                 ('Important dates', {'fields': ('date_joined', 'last_login')}))

    def get_queryset(self, request):
        if request.user.account_type == 'Адміністратор':
            queryset = CustomUser.objects
            return queryset

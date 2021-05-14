from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .forms import UserAdminCreationForm, UserAdminChangeForm
from .models import CustomUser, Following


class CustomUserAdmin(UserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        ('ユーザー情報', {
            'fields': ('username', 'password')
        }),
        ('ユーザー権限', {
            'fields': ('is_active', 'is_staff', 'is_superuser')
        })
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2')
        }),
    )
    list_display = ('username', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Following)
admin.site.unregister(Group)


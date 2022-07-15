from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User


class UserAdminConfig(UserAdmin):
    """Конфигурация админ.панели для работы с пользователями"""
    model = User
    search_fields = ('email', 'name', 'surname',)
    list_filter = ('email', 'name', 'surname', 'is_active', 'is_staff',)
    ordering = ('-signup_date',)
    list_display = ('email', 'signup_date',)
    fieldsets = (
        (None, {'fields': ('email', 'name', 'surname',)}),
        (None, {'fields': ('signup_date',)}),
        ('Доступ', {'fields': ('is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'name', 'surname', 'password1',
                'password2', 'is_active', 'is_superuser', 'is_staff', 'groups',
            )
        }),
    )
    readonly_fields = ('signup_date',)


admin.site.register(User, UserAdminConfig)

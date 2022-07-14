from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """
    Кастомный менеджер пользователей, где для регистрации
    используются почта пользователя вместо имени пользователя
    """
    def create_user(self, email, password=None, **kwargs):
        """Создание пользователя с почтой и паролем"""
        if not email:
            raise ValueError(_("Электронная почта является обязательной для указания"))

        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password, **kwargs):
        """Создание суперпользователя"""
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError(_('У суперпользователя должно быть is_staff=True.'))
        if kwargs.get('is_superuser') is not True:
            raise ValueError(_('У суперпользователя должно быть is_superuser=True.'))

        return self.create_user(email, password, **kwargs)


class User(AbstractBaseUser, PermissionsMixin):
    """Кастомная модель пользователя"""
    name = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Имя"))
    surname = models.CharField(max_length=256, null=True, blank=True, verbose_name=_("Фамилия"))
    email = models.EmailField(unique=True, verbose_name=_("Электронная почта"))
    signup_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата регистрации"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Статус сотрудника"))
    is_active = models.BooleanField(default=False, verbose_name=_("Статус активности"))
    is_superuser = models.BooleanField(default=False, verbose_name=_("Режим суперпользователя"))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

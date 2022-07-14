from django.db import models
from django.utils.translation import gettext_lazy as _


class Tag(models.Model):
    """Модель данных с информацией о теге, привязываемому к статьям"""
    name = models.CharField(max_length=30, verbose_name=_('Название'))
    slug = models.SlugField(max_length=30, verbose_name=_('URL-идентификатор тега'))

    class Meta:
        db_table = 'tags'
        verbose_name = _('Тег')
        verbose_name_plural = _('Теги')

    def __str__(self):
        return self.name

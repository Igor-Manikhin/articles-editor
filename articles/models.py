from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from tags.models import Tag


class Article(models.Model):
    """Модель данных с информацией о создаваемой автором статье"""
    title = models.CharField(max_length=60, verbose_name=_('Заголовок'))
    richtext = models.TextField(verbose_name=_('Текст'))
    banner = models.TextField(verbose_name=_('Изображение баннера в формате base64'))
    author = models.ForeignKey(
        get_user_model(),
        related_name='articles',
        on_delete=models.CASCADE,
        verbose_name=_("Автор")
    )
    tags = models.ManyToManyField(Tag, related_name="articles", verbose_name="Теги", blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated_at = models.DateTimeField(
        auto_now=True, null=True, blank=True, verbose_name=_("Дата редактирования")
    )

    class Meta:
        db_table = 'articles'
        verbose_name = _('Статья')
        verbose_name_plural = _('Статьи')

    def __str__(self):
        return self.title

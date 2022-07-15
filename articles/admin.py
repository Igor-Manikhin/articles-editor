from django.contrib import admin
from django.db.models import QuerySet
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from articles.models import Article


class ArticleAdmin(admin.ModelAdmin):
    """Конфигурация админ.панели для работы со статьями"""
    model = Article
    list_display = ('title', 'author',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'richtext', 'banner', 'author')
        }),
        ('Даты создания и редактирования', {
            'fields': ('created_at', 'updated_at',)
        }),
        (None, {
            'fields': ('tags', 'banner_image',)
        })
    )
    readonly_fields = ('author', 'created_at', 'updated_at', 'banner_image',)

    def get_queryset(self, request) -> QuerySet[Article]:
        articles_queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return articles_queryset

        return articles_queryset.filter(author=request.user).all()

    @admin.display(description=_('Превью баннера'))
    def banner_image(self, obj) -> str:
        return format_html('<img src="data:;base64,{}" width="500" height="350">', mark_safe(obj.banner))

    def save_model(self, request, obj, form, change) -> None:
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Article, ArticleAdmin)

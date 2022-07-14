from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from articles.models import Article


class ArticleAdmin(admin.ModelAdmin):
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

    @admin.display(description=_('Превью баннера'))
    def banner_image(self, obj):
        return format_html('<img src="{}" width="500" height="350">', mark_safe(obj.banner))

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Article, ArticleAdmin)

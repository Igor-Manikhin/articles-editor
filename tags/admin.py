from django.contrib import admin

from tags.models import Tag


class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ('name', 'user',)
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'user',)
        }),
    )
    readonly_fields = ('user',)

    def get_queryset(self, request):
        tags_queryset = super().get_queryset(request)

        if request.user.is_superuser:
            return tags_queryset

        return tags_queryset.filter(user=request.user).all()

    def save_model(self, request, obj, form, change):
        obj.user = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Tag, TagAdmin)

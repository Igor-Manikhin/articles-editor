from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django_filters.rest_framework import FilterSet, CharFilter

from articles.models import Article


class ArticleFilterSet(FilterSet):
    tag = CharFilter(field_name='tags__name', lookup_expr='iexact', label=_("Тег"))
    author = CharFilter(method='filter_by_author', label=_("Автор"))

    class Meta:
        model = Article
        fields = ('tag', 'author')

    @staticmethod
    def filter_by_author(queryset, _, value):
        return queryset.filter(Q(author__name__iexact=value) | Q(author__surname__iexact=value))

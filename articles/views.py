from typing import Type, Union, Optional

from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from articles.filters import ArticleFilterSet
from articles.models import Article
from articles.permissions import IsSuperAdmin, Common
from articles.serializers import ArticleSerializer, ArticleCreateUpdateSerializer


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.select_related(
        'author'
    ).prefetch_related(
        'tags'
    ).only(
        'title',
        'richtext',
        'created_at',
        'updated_at',
        'banner',
        'author__name',
        'author__surname',
        'author__email',
        'tags__name',
        'tags__slug'
    ).all()
    serializer_class = ArticleSerializer
    filterset_class = ArticleFilterSet
    search_fields = ('title', 'tags__name', 'author__name', 'author__surname', 'author__email',)

    def get_permissions(self) -> list:
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [(IsSuperAdmin | Common) & IsAuthenticated]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]

    def get_serializer_class(self) -> Type[Union[ArticleSerializer, ArticleCreateUpdateSerializer]]:
        return ArticleSerializer if self.action in ['retrieve', 'list'] else ArticleCreateUpdateSerializer

    def __create_or_update_instance(
        self,
        request_data: dict,
        instance: Optional[Article] = None,
        partial: bool = False
    ) -> Article:
        request_serializer = self.get_serializer(data=request_data, instance=instance, partial=partial)
        request_serializer.is_valid(raise_exception=True)

        return request_serializer.save()

    def create(self, request, *args, **kwargs) -> Response:
        article_instance = self.__create_or_update_instance(request_data=request.data)
        response_serializer = ArticleSerializer(instance=article_instance)
        headers = self.get_success_headers(response_serializer.data)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )

    def update(self, request, *args, **kwargs) -> Response:
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        updated_article_instance = self.__create_or_update_instance(
            request_data=request.data, instance=instance, partial=partial
        )

        response_serializer = ArticleSerializer(instance=updated_article_instance)
        return Response(response_serializer.data)

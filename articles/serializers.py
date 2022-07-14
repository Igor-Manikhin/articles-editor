from typing import List

from rest_framework import serializers

from articles.models import Article
from tags.models import Tag
from tags.serializers import TagSerializer


class ArticleSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Article
        fields = ('id', 'title', 'richtext', 'banner', 'author', 'created_at', 'updated_at', 'tags',)

    @staticmethod
    def get_author(article: Article) -> str:
        author = article.author
        author_name = ''

        if name := author.name:
            author_name += name

        if surname := author.surname:
            author_name += f" {surname}"

        return author_name


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    tags = serializers.ListField(
        child=serializers.CharField(min_length=1), write_only=True,
        allow_empty=True, required=False, default=[]
    )

    class Meta:
        model = Article
        fields = ('title', 'richtext', 'banner', 'created_at', 'updated_at', 'tags',)

    @staticmethod
    def __set_article_tags(article_instance: Article, tags_names_list: List[str]) -> None:
        if tags_names_list:
            tags_queryset = Tag.objects.only('name').filter(name__in=tags_names_list).all()
            article_instance.tags.set(tags_queryset)

    def create(self, validated_data: dict) -> Article:
        request = self.context.get("request")
        tags_names_list = validated_data.pop('tags')

        article_instance = Article.objects.create(author=request.user, **validated_data)
        self.__set_article_tags(article_instance, tags_names_list)

        return article_instance

    def update(self, instance: Article, validated_data: dict) -> Article:
        tags_names_list = validated_data.pop('tags')
        self.__set_article_tags(instance, tags_names_list)

        for attr_name, attr_value in validated_data.items():
            setattr(instance, attr_name, attr_value)

        instance.save()
        return instance

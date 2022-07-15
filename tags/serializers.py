from rest_framework import serializers

from tags.models import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('name', 'slug',)

    def create(self, validated_data: dict) -> Tag:
        request = self.context.get("request")
        validated_data['user'] = request.user
        return super().create(validated_data)

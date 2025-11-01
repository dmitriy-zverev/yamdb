import re

from rest_framework import serializers

from .models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')

    def validate(self, attrs):
        slug = attrs['slug']
        if Category.objects.filter(slug=slug).exists():
            raise serializers.ValidationError(
                'Сегмент с таким названием уже существует')
        if not re.match(r'^[-a-zA-Z0-9_]+$', slug):
            raise serializers.ValidationError(
                'Неверный формат названия сегмента')
        return attrs

import re
import datetime

from rest_framework import serializers

from .models import Category, Genre, Title


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


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')

    def validate(self, attrs):
        slug = attrs['slug']
        if Genre.objects.filter(slug=slug).exists():
            raise serializers.ValidationError(
                'Жанр с таким названием уже существует')
        if not re.match(r'^[-a-zA-Z0-9_]+$', slug):
            raise serializers.ValidationError('Неверный формат названия жанра')
        return attrs


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(read_only=True)
    genre = serializers.StringRelatedField(read_only=True, many=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')

    def validate(self, attrs):
        year = attrs.get('year', None)
        rating = attrs.get('rating', 0)
        genre = attrs.get('genre', None)
        category = attrs.get('category', None)

        if year is None or year < 0 or year > datetime.date.today().year:
            raise serializers.ValidationError('Неверный формат года')
        if rating < 0 or rating > 10:
            raise serializers.ValidationError('Неверный формат рейтинга')
        if genre is None or genre == []:
            raise serializers.ValidationError('Неверный формат жанра')
        if category is None:
            raise serializers.ValidationError('Неверный формат категории')

        return attrs

    def create(self, validated_data):
        category_slug = self.initial_data.get('category')
        genre_slugs = self.initial_data.get('genre')

        title = Title.objects.create(**validated_data)

        if category_slug:
            category = Category.objects.get(slug=category_slug)
            title.category = category
            title.save(update_fields=['category'])

        if genre_slugs:
            genres = list(Genre.objects.filter(slug__in=genre_slugs))
            title.genre.set(genres)

        return title

    def update(self, instance, validated_data):
        Title.objects.filter(pk=instance.pk).update(**validated_data)

        category_slug = self.initial_data.get('category')
        genre_slugs = self.initial_data.get('genre')

        if category_slug:
            category = Category.objects.get(slug=category_slug)
            instance.category = category
            instance.save(update_fields=['category'])

        if genre_slugs:
            genres = list(Genre.objects.filter(slug__in=genre_slugs))
            instance.genre.set(genres)

        instance.refresh_from_db()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['category'] = CategorySerializer(instance.category).data
        data['genre'] = GenreSerializer(instance.genre.all(), many=True).data

        return data

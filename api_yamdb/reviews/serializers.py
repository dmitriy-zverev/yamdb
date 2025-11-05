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

    def validate_rating(self, value):
        if value < 0 or value > 10:
            raise serializers.ValidationError('Неверный формат рейтинга')
        return value

    def validate(self, attrs):
        year = attrs.get('year', None)

        if self.instance is None and year is None:
            raise serializers.ValidationError('Неверный формат года')

        if year is not None and (year < 0
                                 or year > datetime.date.today().year):
            raise serializers.ValidationError('Неверный формат года')
        return attrs

    def create(self, validated_data):
        category_slug = self.initial_data.get('category', None)
        genre_slugs = self.initial_data.get('genre', None)

        if genre_slugs is None or genre_slugs == []:
            raise serializers.ValidationError(
                {'genre': 'Неверный формат жанра'})
        if category_slug is None:
            raise serializers.ValidationError(
                {'category': 'Неверный формат категории'})

        category = Category.objects.get(slug=category_slug)
        genres = list(Genre.objects.filter(slug__in=genre_slugs))

        if len(genres) != len(genre_slugs):
            raise serializers.ValidationError(
                {'genre': 'Таких жанров не существует'})
        if category is None:
            raise serializers.ValidationError(
                {'category': 'Такой категории не существует'})

        title = Title.objects.create(**validated_data)

        if category_slug:
            title.category = category
            title.save(update_fields=['category'])

        if genre_slugs:
            title.genre.set(genres)

        return title

    def update(self, instance, validated_data):
        Title.objects.filter(pk=instance.pk).update(**validated_data)

        category_slug = self.initial_data.get('category')
        genre_slugs = self.initial_data.get('genre')

        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
            except Category.DoesNotExist:
                raise serializers.ValidationError(
                    f"Категория с слагом '{category_slug}' не найдена")
            instance.category = category
            instance.save(update_fields=['category'])

        if genre_slugs:
            genres = list(Genre.objects.filter(slug__in=genre_slugs))
            if len(genres) != len(genre_slugs):
                raise serializers.ValidationError(
                    {'genre': 'Таких жанров не существует'})
            instance.genre.set(genres)

        instance.refresh_from_db()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data['category'] = CategorySerializer(instance.category).data
        data['genre'] = GenreSerializer(instance.genre.all(), many=True).data

        return data

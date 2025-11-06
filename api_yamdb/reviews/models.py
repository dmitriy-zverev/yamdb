from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=256)
    year = models.IntegerField(default=0)
    rating = models.FloatField(default=0)
    description = models.TextField(default='')
    genre = models.ManyToManyField(
        'Genre',
        related_name='titles',
        blank=True,
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='titles',
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        related_name='reviews',
    )
    score = models.IntegerField()
    pub_date = models.DateTimeField(blank=True)
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews')

    def __str__(self):
        return f'{self.text}: {self.author}'

import datetime

from rest_framework import viewsets, filters
from rest_framework.exceptions import PermissionDenied, ValidationError

from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import (
    Category,
    Genre,
    Title,
    Review,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    ReviewSerializer,
)
from .filters import TitleFilter

from api.permissions import (
    ReadOnlyOrAdmin,
    ReadOnlyOrAuthenticated,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [ReadOnlyOrAdmin]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['name', 'slug']
    search_fields = ['name', 'slug']
    http_method_names = ['get', 'post', 'delete']


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [ReadOnlyOrAdmin]
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter]
    filterset_fields = ['name', 'slug']
    search_fields = ['name', 'slug']
    http_method_names = ['get', 'post', 'delete']


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = [ReadOnlyOrAdmin]
    lookup_field = 'id'
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_class = TitleFilter
    http_method_names = ['get', 'post', 'patch', 'delete']


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [ReadOnlyOrAuthenticated]
    lookup_field = 'id'
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]
    filterset_fields = ['text', 'score']
    search_fields = ['text', 'score']
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Review.objects.filter(title_id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs['title_id'])
        if Review.objects.filter(author=self.request.user, title=title):
            raise ValidationError({'text': 'Нельзя создать второй отзыв'})

        serializer.save(title=title,
                        author=self.request.user,
                        pub_date=datetime.datetime.now())

    def perform_update(self, serializer):
        instance = self.get_object()
        if (self.request.user != instance.author
                and self.request.user.role not in ['admin', 'moderator']):
            raise PermissionDenied('Вы не можете редактировать чужой отзыв')
        serializer.save()

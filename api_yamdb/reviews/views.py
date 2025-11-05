from rest_framework import viewsets, filters

from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    Category,
    Genre,
    Title,
)
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
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

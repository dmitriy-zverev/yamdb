from rest_framework import viewsets, filters

from .models import Category, Genre
from .serializers import CategorySerializer, GenreSerializer

from api.permissions import ReadOnlyOrAdmin


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

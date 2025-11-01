from rest_framework import viewsets, filters

from .models import Category
from .serializers import CategorySerializer

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

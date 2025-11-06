from rest_framework import routers
from rest_framework_nested import routers as nested_routers
from django.urls import path, include

from .views import (
    SignupView,
    ObtainTokenByCodeView,
    UserViewSet,
    SigninView,
)

from reviews.views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet,
    ReviewViewSet,
    CommentViewSet,
)

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

titles_router_v1 = nested_routers.NestedDefaultRouter(router_v1,
                                                      r'titles',
                                                      lookup='title')
titles_router_v1.register(r'reviews', ReviewViewSet, basename='reviews')

reviews_router_v1 = nested_routers.NestedDefaultRouter(titles_router_v1,
                                                       r'reviews',
                                                       lookup='review')
reviews_router_v1.register(r'comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/', include(titles_router_v1.urls)),
    path('v1/', include(reviews_router_v1.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='auth-signup'),
    path('v1/auth/signin/', SigninView.as_view(), name='auth-signin'),
    path('v1/auth/token/', ObtainTokenByCodeView.as_view(), name='auth-token'),
]

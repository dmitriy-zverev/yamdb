from django.urls import path, include
from rest_framework import routers

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
)

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='auth-signup'),
    path('v1/auth/signin/', SigninView.as_view(), name='auth-signin'),
    path('v1/auth/token/', ObtainTokenByCodeView.as_view(), name='auth-token'),
]

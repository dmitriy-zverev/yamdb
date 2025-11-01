from django.urls import path, include
from rest_framework import routers

from .views import (
    SignupView,
    ObtainTokenByCodeView,
    UserViewSet,
)

from reviews.views import (
    CategoryViewSet,
    GenreViewSet,
)

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet)
router_v1.register('categories', CategoryViewSet)
router_v1.register('genres', GenreViewSet)

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='auth-signup'),
    path('v1/auth/token/', ObtainTokenByCodeView.as_view(), name='auth-token'),
]

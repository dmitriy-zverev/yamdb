from django.urls import path, include
from rest_framework import routers

from .views import SignupView, ObtainTokenByCodeView

router_v1 = routers.DefaultRouter()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/signup/', SignupView.as_view(), name='auth-signup'),
    path('v1/auth/token/', ObtainTokenByCodeView.as_view(), name='auth-token'),
]

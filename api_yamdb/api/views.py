from rest_framework import status, permissions, viewsets, filters
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import (
    SignupSerializer,
    TokenByCodeSerializer,
    UserSerializer,
    SigninSerializer,
)
from .models import User
from .permissions import IsAdminRole


class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                'email': serializer.validated_data['email'],
                'username': serializer.validated_data['username'],
            },
            status=status.HTTP_200_OK)


class ObtainTokenByCodeView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = TokenByCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        if not user.is_active:
            user.is_active = True
            user.save(update_fields=['is_active'])

        refresh = RefreshToken.for_user(user)
        access = refresh.access_token
        return Response({'token': str(access)}, status=status.HTTP_200_OK)


class SigninView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = SigninSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'username': serializer.validated_data['username'],
        })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    lookup_field = 'username'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['username', 'email', 'role']
    search_fields = ['username', 'email', 'role']
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(detail=False,
            methods=['get', 'patch'],
            url_path='me',
            permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        if request.method.lower() == 'get':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)

        serializer = self.get_serializer(request.user,
                                         data=request.data,
                                         partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        instance = self.get_object()
        serializer = self.get_serializer(instance,
                                         data=request.data,
                                         partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

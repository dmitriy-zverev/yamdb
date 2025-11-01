import re

from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import serializers

from .models import User

RESERVED_USERNAMES = ['me']
MAX_USERNAME_LENGTH = 150
MAX_EMAIL_LENGTH = 254


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'role',
                  'bio')

    def validate_username(self, value):
        if len(value) == 0 or len(value) > MAX_USERNAME_LENGTH:
            raise serializers.ValidationError(
                'Имя пользователя содержит недопустимые символы')
        if (value in RESERVED_USERNAMES
                or User.objects.filter(username=value).exists()):
            raise serializers.ValidationError('Имя пользователя занято')
        return value

    def validate_email(self, value):
        if len(value) == 0 or len(value) > MAX_EMAIL_LENGTH:
            raise serializers.ValidationError(
                'Неверный формат электронной почты')
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Эта почта уже используется')
        return value

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = request.user

        if not (user and user.is_authenticated and user.is_admin):
            validated_data.pop('role', None)

        return super().update(instance, validated_data)


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, attrs):
        username = attrs['username']
        email = attrs['email']

        username_exists = User.objects.filter(username=username).exists()
        email_exists = User.objects.filter(email=email).exists()
        if not re.match(r'^[\w.@+-]+\Z', username):
            raise serializers.ValidationError(
                {'username': 'Имя пользователя содержит недопустимые символы'})
        if username in RESERVED_USERNAMES:
            raise serializers.ValidationError(
                {'username': 'Имя пользователя занято'})
        if username_exists and email_exists:
            raise serializers.ValidationError({
                'username':
                'Имя пользователя или почта уже используются',
                'email':
                'Имя пользователя или почта уже используются',
            })
        if username_exists and not email_exists:
            raise serializers.ValidationError(
                {'username': 'Имя пользователя занято'})
        if email_exists and not username_exists:
            raise serializers.ValidationError(
                {'email': 'Эта почта уже используется'})
        if len(username) > MAX_USERNAME_LENGTH:
            raise serializers.ValidationError(
                {'username': 'Имя пользователя слишком длинное'})
        if len(email) > MAX_EMAIL_LENGTH:
            raise serializers.ValidationError(
                {'email': 'Почта слишком длинная'})
        return attrs

    def create(self, validated_data):
        user = User(username=validated_data['username'],
                    email=validated_data['email'],
                    is_active=False)
        user.set_unusable_password()
        user.save()

        code = default_token_generator.make_token(user)
        send_mail(
            subject='Код подтверждения регистрации',
            message=f'Ваш код подтверждения: {code}',
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            recipient_list=[user.email],
            fail_silently=False,
        )
        return user


class TokenByCodeSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    def validate(self, attrs):
        username = attrs['username']
        code = attrs['confirmation_code']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'username': 'Пользователь не найден'})

        if not default_token_generator.check_token(user, code):
            raise serializers.ValidationError(
                {'confirmation_code': 'Неверный или просроченный код'})

        attrs['user'] = user
        return attrs

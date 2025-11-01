from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        USER = 'user', 'Обычный пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'

    role = models.CharField(max_length=20,
                            choices=Role.choices,
                            default=Role.USER)
    bio = models.TextField(max_length=1000, blank=True)

    def __str__(self):
        return f'{self.username}: {self.role}'

    @property
    def is_admin(self):
        return (self.is_superuser or self.is_staff
                or self.role == self.Role.ADMIN)

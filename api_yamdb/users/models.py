from django.contrib.auth.models import AbstractUser
from django.db import models

from api.validators import user_regex_validator


class User(AbstractUser):

    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER_ROLES = [(USER, 'user'), (MODERATOR, 'moderator'), (ADMIN, 'admin')]
    username = models.CharField(blank=False,
                                max_length=150,
                                unique=True,
                                validators=[user_regex_validator],
                                verbose_name='Пользователь')

    bio = models.TextField(verbose_name='Биография', blank=True)
    email = models.EmailField(
        verbose_name='Электронная почта',
        max_length=254,
        unique=True,
        blank=False)
    first_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Имя')
    last_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name='Фамилия')
    role = models.CharField(
        max_length=9,
        choices=USER_ROLES,
        default='user',
        verbose_name='Роль')

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('username', )

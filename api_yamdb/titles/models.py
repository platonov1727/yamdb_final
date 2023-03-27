from django.db import models


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ('slug', )

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название')
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('slug', )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название')
    year = models.IntegerField(verbose_name='Год')
    description = models.TextField(verbose_name='Описание')
    genre = models.ManyToManyField(
        Genre,
        through='GenreTitle',
        verbose_name='Жанр')
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='titles',
        verbose_name='Категория')
    rating = models.IntegerField(
        null=True,
        default=None,
        verbose_name='Рейтинг')

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ('-year', )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        verbose_name='Жанр')
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name='Произведение')

    class Meta:
        verbose_name = 'Жанр-Произведение'
        verbose_name_plural = 'Жанры-Произведения'

    def __str__(self):
        return f'{self.title} в жанре {self.genre}'

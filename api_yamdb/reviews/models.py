from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from users.models import User
from titles.models import Title


class Review(models.Model):
    title = models.ForeignKey(Title,
                              on_delete=models.CASCADE,
                              related_name='reviews',
                              verbose_name='Произведение')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='rewiews',
                               verbose_name='Автор')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    db_index=True,
                                    verbose_name='Дата публикации')
    score = models.PositiveSmallIntegerField(
        'Рейтинг', validators=[MinValueValidator(1),
                               MaxValueValidator(10)])

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review'),
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='автор')
    text = models.TextField(max_length=500, verbose_name='Текст')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    db_index=True,
                                    verbose_name='Дата публикации')
    review = models.ForeignKey(Review,
                               on_delete=models.CASCADE,
                               related_name='comments',
                               verbose_name='Комментарий')

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('pub_date',)

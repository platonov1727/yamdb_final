from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export import widgets

from reviews.models import Review, Comment
from .models import Title


class ReviewResource(resources.ModelResource):
    pub_date = Field(
        attribute='pub_date',
        column_name='pub_date',
        widget=widgets.DateTimeWidget('%Y-%m-%dT%H:%M:%S.%fZ')
    )
    title = Field(
        attribute='title',
        column_name='title_id',
        widget=widgets.ForeignKeyWidget(Title)
    )

    class Meta:
        model = Review
        fields = (
            'id',
            'title',
            'text',
            'author',
            'score',
            'pub_date',
        )


class ReviewAdmin(ImportExportModelAdmin):
    resource_classes = [ReviewResource]
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'id',
        'title',
        'text',
        'author',
        'score',
        'pub_date',
    )

    # Добавляем интерфейс для поиска
    search_fields = ('text',)
    empty_value_display = '-пусто-'


class CommentResource(resources.ModelResource):
    review = Field(
        attribute='review',
        column_name='review_id',
        widget=widgets.ForeignKeyWidget(Review)
    )
    pub_date = Field(
        attribute='pub_date',
        column_name='pub_date',
        widget=widgets.DateTimeWidget('%Y-%m-%dT%H:%M:%S.%fZ')
    )

    class Meta:
        model = Comment
        fields = (
            'id',
            'review',
            'text',
            'author',
            'pub_date',
        )


class CommentAdmin(ImportExportModelAdmin):
    resource_classes = [CommentResource]
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'id',
        'review',
        'text',
        'author',
        'pub_date',
    )

    # Добавляем интерфейс для поиска
    search_fields = ('text',)
    empty_value_display = '-пусто-'


admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)

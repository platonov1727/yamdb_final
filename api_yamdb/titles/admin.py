from django.contrib import admin
from import_export import resources
from import_export import widgets
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field

from .models import Title, Genre, Category, GenreTitle


class TitleResource(resources.ModelResource):

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'category',
        )


class TitleAdmin(ImportExportModelAdmin):
    resource_classes = [TitleResource]
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'id',
        'name',
        'year',
        'category',
    )

    # Добавляем интерфейс для поиска
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class GenreResource(resources.ModelResource):

    class Meta:
        model = Genre
        fields = (
            'id',
            'name',
            'slug',
        )


class GenreAdmin(ImportExportModelAdmin):
    resource_classes = [GenreResource]
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'id',
        'name',
        'slug',
    )

    # Добавляем интерфейс для поиска
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class CategoryResource(resources.ModelResource):

    class Meta:
        model = Category
        fields = (
            'id',
            'name',
            'slug',
        )


class CategoryAdmin(ImportExportModelAdmin):
    resource_classes = [CategoryResource]
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'id',
        'name',
        'slug',
    )

    # Добавляем интерфейс для поиска
    search_fields = ('name',)
    empty_value_display = '-пусто-'


class GenreTitleResource(resources.ModelResource):
    genre = Field(
        attribute='genre',
        column_name='genre_id',
        widget=widgets.ForeignKeyWidget(Genre)
    )
    title = Field(
        attribute='title',
        column_name='title_id',
        widget=widgets.ForeignKeyWidget(Title)
    )

    class Meta:
        model = GenreTitle
        fields = (
            'id',
            'genre',
            'title',
        )


class GenreTitleAdmin(ImportExportModelAdmin):
    resource_classes = [GenreTitleResource]
    # Перечисляем поля, которые должны отображаться в админке
    list_display = (
        'id',
        'genre',
        'title',
    )

    empty_value_display = '-пусто-'


admin.site.register(Title, TitleAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)

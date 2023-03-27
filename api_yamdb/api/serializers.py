from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review
from titles.models import Category, Genre, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class TitleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(required=True,
                             many=True,
                             slug_field='slug',
                             queryset=Genre.objects.all())
    category = SlugRelatedField(required=False,
                                slug_field='slug',
                                queryset=Category.objects.all())

    class Meta:
        fields = ('id', 'name', 'year', 'rating', 'description', 'genre',
                  'category')
        model = Title


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'
        extra_kwargs = {'url': {'lookup_field': 'slug'}}


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    author = serializers.SlugRelatedField(
        default=serializers.CurrentUserDefault(),
        slug_field='username',
        read_only=True)

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise ValidationError('Только один отзыв на произведение!')
        return data

    class Meta:
        model = Review
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    review = serializers.SlugRelatedField(slug_field='text', read_only=True)
    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        model = Comment
        fields = '__all__'


class ReadOnlyTitleSerializer(serializers.ModelSerializer):
    rating = serializers.IntegerField(source='reviews__score__avg',
                                      read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        model = Title
        fields = '__all__'

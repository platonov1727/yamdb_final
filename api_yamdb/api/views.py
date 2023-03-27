from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.pagination import PageNumberPagination
from titles.models import Category, Genre, Title
from reviews.models import Review
from rest_framework import mixins

from .filters import TitlesFilter
from .permissions import IsAdminOrReadOnly, IsAdminModeratorOwnerOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          ReadOnlyTitleSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    serializer_class = TitleSerializer
    queryset = Title.objects.all().annotate(
        Avg("reviews__score")).order_by("name")
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitlesFilter
    permission_classes = (IsAdminOrReadOnly, )

    def get_serializer_class(self):
        if self.action in ("retrieve", "list"):
            return ReadOnlyTitleSerializer
        return TitleSerializer


class ListCreateDestroyViewSet(
        mixins.CreateModelMixin, mixins.DestroyModelMixin,
        mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class GenreViewSet(ListCreateDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = 'slug'


class CategoryViewSet(ListCreateDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    permission_classes = (IsAdminOrReadOnly, )
    lookup_field = 'slug'


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdminModeratorOwnerOrReadOnly]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get("title_id"))

        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)

from typing import List
from rest_framework import permissions, viewsets

from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.filters import SearchFilter

from reviews.models import Title, Category, Genre, Title
from users.models import User
from .serializers import ReviewSerializer, CommentSerializer, UserSerializer, CategorySerializer, GenreSerializer, TitleSerializer, TitleCreateSerializer
from .permissions import AuthorOrModeratorOrAdminOrReadOnly, ReadOrAdminOnly


class ReviewViewSet(viewsets.ModelViewSet):

    """
    Предоставляет возможность работать с отзывами к произведениям:
    читать, создавать, редактировать, удалять.
    Координирует разрешения на доступ.
    """

    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrModeratorOrAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = title.reviews.all()
        return review

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=get_object_or_404(
                Title, id=self.kwargs['title_id']
            )
        )


class CommentViewSet(viewsets.ModelViewSet):

    """
    Предоставляет возможность работать с комментариями к отзывам:
    читать, создавать, редактировать, удалять.
    Координирует разрешения на доступ по ролям.
    """

    serializer_class = CommentSerializer
    permission_classes = (AuthorOrModeratorOrAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        review = title.reviews.all()
        return review

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=get_object_or_404(
                Title, id=self.kwargs['title_id']
            )
        )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CategoryViewSet(ListModelMixin, CreateModelMixin,
                      DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    permission_classes = (ReadOrAdminOnly,)


class GenreViewSet(ListModelMixin, CreateModelMixin,
                   DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    permission_classes = (ReadOrAdminOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('title_id_reviews__score'))
    filter_backends = (SearchFilter,)
    search_fields = ['category', 'genre', 'name', 'year']
    pagination_class = PageNumberPagination
    permission_classes = (ReadOrAdminOnly,)


    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer

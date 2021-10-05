from rest_framework import viewsets

from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Title
from .serializers import ReviewSerializer, CommentSerializer
from .permissions import AuthorOrModeratorOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (AuthorOrModeratorOrReadOnly,)
    pagination_class = LimitOffsetPagination
    ordering_fields = ('score',)
    ordering = ('-score',)

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
    serializer_class = CommentSerializer
    permission_classes = (AuthorOrModeratorOrReadOnly)
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

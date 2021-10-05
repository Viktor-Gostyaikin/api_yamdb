from rest_framework import viewsets

from django.shortcuts import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination

from reviews.models import Title
from users.models import User
from .serializers import ReviewSerializer, CommentSerializer, UserSerializer
from .permissions import AuthorOrModeratorOrAdminOrReadOnly


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
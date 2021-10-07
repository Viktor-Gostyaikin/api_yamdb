from rest_framework import viewsets

from django.shortcuts import get_object_or_404
#from rest_framework.pagination import LimitOffsetPagination
from rest_framework.mixins import CreateModelMixin
#from rest_framework.permissions import IsAuthenticatedOrReadOnly

from reviews.models import Title, Review
from users.models import User
from .serializers import ReviewSerializer, CommentSerializer, UserSerializer
#from .permissions import AuthorOrModeratorOrAdminOrReadOnly


class ReviewViewSet(viewsets.ModelViewSet, CreateModelMixin):

    """
    Предоставляет возможность работать с отзывами к произведениям:
    читать, создавать, редактировать, удалять.
    Координирует разрешения на доступ.
    """

    serializer_class = ReviewSerializer
    #permission_classes = (IsAuthenticatedOrReadOnly,)
    #pagination_class = LimitOffsetPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs['title_id'])
        return title.title_reviews.all()

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
    #permission_classes = (IsAuthenticatedOrReadOnly,)
    #pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs['review_id'])
        comments = review.review_comments.all()
        return comments

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user, title=get_object_or_404(
                Title, id=self.kwargs['title_id']
            )
        )


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

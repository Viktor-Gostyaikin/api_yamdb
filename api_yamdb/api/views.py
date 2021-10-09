from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_simplejwt.views import TokenObtainPairView

from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404

from reviews.models import Title
from users.models import User
from .serializers import (
    ReviewSerializer, CommentSerializer, UserSerializer,
    UserRegistrationSerializer, YaTokenSerializer,
)
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
        review = title.title_reviews.all()
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


class GetTokennView(TokenObtainPairView):
    serializer_class = YaTokenSerializer


@api_view(['POST'])
def create_auth_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        new_user = User.objects.get(username=request.data['username'])
        confirmation_code = new_user.make_confirmation_code()
        new_user.set_confirmation_code(confirmation_code=confirmation_code)
        new_user.save()
        new_user.email_user(
            subject='Подтверждение регистрации',
            message=f'Ваш confirmation code {confirmation_code}',
            from_email=settings.EMAIL_HOST_USER,
        )
        return Response('Отправлено письмо с confirmation_code на ваш email', status=status.HTTP_201_CREATED)
    else:
        return Response(serializer._errors, status=status.HTTP_400_BAD_REQUEST)

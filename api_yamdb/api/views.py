from django.contrib.auth import get_user_model
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import permissions, viewsets, status, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.mixins import ListModelMixin, CreateModelMixin, DestroyModelMixin
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Title, Category, Genre
from .serializers import (
    ReviewSerializer, CommentSerializer, UserSerializer,
    UserMeSerializer, UserRegistrationSerializer,
    GetTokenSerializer, CategorySerializer, GenreSerializer,
    TitleSerializer, TitleCreateSerializer,
)
from .permissions import AdminOnly, AuthorOrModeratorOrAdminOrReadOnly, ReadOrAdminOnly

User = get_user_model()

class ReviewViewSet(viewsets.ModelViewSet):

    '''
    Предоставляет возможность работать с отзывами к произведениям:
    читать, создавать, редактировать, удалять.
    Координирует разрешения на доступ.
    '''

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

    '''
    Предоставляет возможность работать с комментариями к отзывам:
    читать, создавать, редактировать, удалять.
    Координирует разрешения на доступ по ролям.
    '''

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


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AdminOnly(),)
    pagination_class = LimitOffsetPagination
    filter_backends = (SearchFilter,)
    search_fields = ['username']
    lookup_field = 'username'

    def get_queryset(self):
        user = self.request.user
        if self.action == 'me':
            self.queryset = self.queryset.filter(pk=user.pk)
        return self.queryset
    
    def get_permissions(self):
        if self.action == 'me':
            return  (permissions.IsAuthenticated()),
        return self.permission_classes

    def get_serializer_class(self):
        if self.action == 'me':
            return UserMeSerializer
        return self.serializer_class

    def get_instance(self):
        return self.request.user

    @action(['get', 'put', 'patch', 'delete'], detail=False)
    def me(self, request, *args, **kwargs):
        self.get_object = self.get_instance
        if request.method == 'GET':
            return self.retrieve(request, *args, **kwargs)
        elif request.method == 'PUT':
            return self.update(request, *args, **kwargs)
        elif request.method == 'PATCH':
            return self.partial_update(request, *args, **kwargs)
        elif request.method == 'DELETE':
            return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class GetTokenView(TokenObtainPairView):
    serializer_class = GetTokenSerializer


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


class CategoryViewSet(
    ListModelMixin, CreateModelMixin,
    DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    permission_classes = (ReadOrAdminOnly,)


class GenreViewSet(
    ListModelMixin, CreateModelMixin,
    DestroyModelMixin, viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['name']
    pagination_class = LimitOffsetPagination
    lookup_field = 'slug'
    permission_classes = (ReadOrAdminOnly,)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('title_reviews__score'))
    filter_backends = (SearchFilter,)
    search_fields = ['category', 'genre', 'name', 'year']
    pagination_class = PageNumberPagination
    permission_classes = (ReadOrAdminOnly,)


    def get_serializer_class(self):
        if self.action in ('create', 'update', 'partial_update'):
            return TitleCreateSerializer
        return TitleSerializer

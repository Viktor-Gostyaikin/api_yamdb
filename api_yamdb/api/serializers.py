from django.db.models import fields
from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from rest_framework.relations import SlugRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
from django.conf import settings
from reviews.models import Review, Comment, Category, Genre, Title

from users.models import User
from django.contrib.auth import authenticate

UNIQUE_REVIEW = 'Вы уже оставили отзыв к данному произведению'
ERROR_SCORE = 'Оценка произведения должна быть в значении от 1 до 10'


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='id',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate_score(self, value):
        if not (1 < value < 10):
            raise serializers.ValidationError(ERROR_SCORE)
        return value

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id')
        ).exists():
            raise ValidationError(UNIQUE_REVIEW)
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='id'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',

        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
        def validate_role(self, value):
            if value.lower() in [User.MODERATOR, User.USER, User.ADMIN]:
                raise serializers.ValidationError('Invalid value of role')
            return value


class UserMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',

        )
        read_only_fields = ['role']
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

        def validate_role(self, value):
            if value.lower() in [User.MODERATOR, User.USER, User.ADMIN]:
                raise serializers.ValidationError('Invalid value of role')
            return value


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]
    def validate_username(self, value):
        """
        Check that the username not a 'me'.
        """
        if 'me' == value.lower():
            raise serializers.ValidationError('Invalid value of username')
        return value


class GetTokenSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        self.fields[self.username_field] = serializers.CharField()
        self.fields['confirmation_code'] = PasswordField()
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['access'] = user.name
        return token

    def validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: attrs[self.username_field],
            'confirmation_code': attrs['confirmation_code'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not settings.api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )
        if self.user.is_authenticated:
            return self.user.token

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)
    rating = serializers.FloatField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title



class TitleCreateSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        many=True,
        slug_field='slug',
        queryset=Genre.objects.all()
    )
    class Meta:
        fields = '__all__'
        model = Title

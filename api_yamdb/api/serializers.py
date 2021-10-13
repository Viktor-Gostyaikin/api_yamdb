from django.contrib.auth import get_user_model

from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator, ValidationError
from rest_framework.relations import SlugRelatedField
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Review, Comment, Category, Genre, Title


UNIQUE_REVIEW = 'Вы уже оставили отзыв к данному произведению'
ERROR_SCORE = 'Оценка произведения должна быть в значении от 1 до 10'

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

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

    def validate_email(self, value):
        try:
            if User.objects.get(email=value):
                raise serializers.ValidationError('Email is occupied')
        except User.DoesNotExist:
            return value


class ConfirmationCodeField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})

        kwargs['style']['input_type'] = 'confirmation_code'
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)


class GetTokenSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150,)
    confirmation_code = ConfirmationCodeField()

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate_username(self, value):
        try:
            if User.objects.get(username=value):
                return value
        except User.DoesNotExist:
            raise exceptions.NotFound()

    def validate(self, attrs):
        try:
            attrs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = User.objects.get(username=attrs['username'])
        if self.user.check_confirmation_code(attrs['confirmation_code']):
            refresh = self.get_token(self.user)
            return {'access': str(refresh.access_token)}
        raise serializers.ValidationError('The data is not valid')


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


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        read_only_fields = ('id', 'author', 'pub_date')

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
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        #read_only_fields = ('id', 'author', 'pub_date')

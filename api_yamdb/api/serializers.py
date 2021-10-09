from rest_framework import serializers, exceptions
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.relations import SlugRelatedField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, PasswordField
from django.conf import settings
from reviews.models import Review, Comment
from users.models import User
from django.contrib.auth import authenticate


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='id',
    )
    title = SlugRelatedField(
        read_only=True,
        slug_field='id',
    )

    class Meta:
        model = Review
        fields = ('__all__')

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title')
            )
        ]

    def get_average_score(self, obj):
        reviews = Review.objects.filter(obj.title)
        return round(sum(reviews.score) / len(reviews.score))


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='id'
    )
    review = SlugRelatedField(
        read_only=True, slug_field='id'
    )

    class Meta:
        model = Comment
        fields = ('__all__')


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
            'role'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]


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

class YaTokenSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

        return {}
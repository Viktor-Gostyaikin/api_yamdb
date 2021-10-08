from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import Review, Comment
from users.models import User

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

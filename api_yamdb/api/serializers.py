from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import Review, Comment
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='id',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        if Review.objects.filter(
            author=self.context['request'].user,
            title=self.context['view'].kwargs.get('title_id')
        ).exists():
            raise ValidationError('Вы уже оставили отзыв к данному произведению')
        return data

    """def get_score(self, obj):
        reviews = Review.objects.filter(obj.title)
        return round(sum(reviews.score) / len(reviews.score))"""


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

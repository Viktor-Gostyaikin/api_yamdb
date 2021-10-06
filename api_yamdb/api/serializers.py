from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.relations import SlugRelatedField

from reviews.models import Review, Comment
from users.models import User

class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True,
        slug_field='user_id',
    )
    title_id = SlugRelatedField(
        read_only=True,
        slug_field='title_id',
    )

    class Meta:
        model = Review
        fields = ('__all__')

        validators = [
            UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=('author', 'title_id')
            )
        ]

    def get_average_score(self, obj):
        reviews = Review.objects.filter(obj.title_id)
        return round(sum(reviews.score) / len(reviews.score))


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='user_id'
    )
    review = SlugRelatedField(
        read_only=True, slug_field='review_id'
    )

    class Meta:
        model = Comment
        fields = ('__all__')


class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')
        validators = [
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework.relations import SlugRelatedField

from reviews.models import Review, Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='user_id'
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
    class Meta:
        model = Comment
        fields = ('__all__')

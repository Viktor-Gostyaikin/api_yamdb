from django.db import models

from users.models import User


class Title(models.Model):
    name = None
    year = None
    category = None


class Review(models.Model):
    title_id = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title_id_reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_reviews'
    )
    score = models.SmallIntegerField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['title_id', 'author'],
                                    name='unique_review')
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='review_comments',
        db_index=True
    )
    text = models.TextField()

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_comments',
        db_index=True
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )


class Category(models.Model):
    name = None
    slug = None


class Genre(models.Model):
    name = None
    slug = None


class Genre_Title(models.Model):
    title_id = None
    genre_id = None

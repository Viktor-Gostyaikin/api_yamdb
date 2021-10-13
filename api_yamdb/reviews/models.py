from django.db import models

from users.models import User
from .validators import validator_year


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True,
                            verbose_name='Категория')
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=256, unique=True, verbose_name='Жанр')
    slug = models.SlugField(max_length=56, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(max_length=100, verbose_name='Произведение')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="titles"
    )
    genre = models.ManyToManyField(Genre, related_name="titles")
    year = models.IntegerField(
        verbose_name="Год издания", db_index=True,
        validators=[validator_year],
    )

    description = models.CharField(max_length=300, null=True)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='title_reviews',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_reviews',
    )
    score = models.SmallIntegerField()
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

        constraints = [
            models.UniqueConstraint(fields=['title', 'author'],
                                    name='unique_review')
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='review_comments')
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='author_comments',
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True)

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text

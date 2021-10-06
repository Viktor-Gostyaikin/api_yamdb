from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=256, unique=True,
                            verbose_name='категория')
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
    name = models.CharField(max_length=256, verbose_name='произведения')
    year = models.IntegerField(
        verbose_name="Год издания", db_index=True, default='2021')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="titles")

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Genre_Title(models.Model):
    title_id = models.ForeignKey(
        Title, on_delete=models.CASCADE,
        related_name="titles", default=1)
    genre_id = models.ForeignKey(
        Genre, related_name="ganre", on_delete=models.CASCADE, default=1)


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

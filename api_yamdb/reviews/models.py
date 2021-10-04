from django.db import models
from django.contrib.auth import get_user_model
#from .users.models import User

User = get_user_model()

SCORE = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)


class Review(models.Model):
    text = models.CharField(max_lengt=10000)
    score = models.CharField(max_lengt=2, choices=SCORE)
    author = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='reviews')
    pub_date = models.DateTimeField('Дата публикации', auto_now_add=True)


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments')
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        db_index=True
    )
    text = models.TextField(max_lengt=10000)
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

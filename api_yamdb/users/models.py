import jwt
from django.contrib.auth.hashers import make_password
from django.conf import settings
from datetime import datetime
from django.utils.crypto import get_random_string
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'Пользователь'),
        (MODERATOR, 'Модератор'),
        (ADMIN, 'Администратор'),
    )
    email = models.EmailField(
        'email address', max_length=254, blank=False, unique=True)
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True,
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    role = models.CharField(
        'Роль', choices=ROLE_CHOICES, max_length=9, default=USER
    )
    confirmation_code = models.CharField(
        'confirmation_code', blank=True, max_length=128)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    objects = UserManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_user')
        ]

    @property
    def token(self):

        """
        Позволяет получить токен пользователя путем вызова user.token, вместо
        user._generate_jwt_token(). Декоратор @property выше делает это
        возможным. token называется "динамическим свойством".
        """

        return self._generate_jwt_token()

    def _generate_jwt_token(self):

        """
        Генерирует веб-токен JSON, в котором хранится идентификатор этого
        пользователя, срок действия токена составляет 1 день от создания
        """

        dt = datetime.now() + datetime.timedelta(days=1)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def get_full_name(self):

        """
        Этот метод требуется Django для таких вещей, как обработка электронной
        почты. Обычно это имя фамилия пользователя, но поскольку мы не
        используем их, будем возвращать username.
        """

        return self.username

    def set_confirmation_code(self, confirmation_code):
        self.confirmation_code = make_password(confirmation_code)

    def make_confirmation_code(
        self, length=6,
        allowed_chars='abcdefghjkmnpqrstuvwxyz'
            'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    ):

        """
        Generate a random password with the given length and given
        allowed_chars. The default value of allowed_chars does not have "I" or
        "O" or letters and digits that look similar -- just to avoid confusion.
        """

        return get_random_string(length, allowed_chars)

import datetime as dt

from django.core.exceptions import ValidationError


def validator_year(val):
    current_year = dt.date.today().year
    if val > current_year:
        raise ValidationError('Такой год еще не наступил')

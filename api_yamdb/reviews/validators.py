import datetime

from django.core.exceptions import ValidationError


def validator_year(val):
    current_year = datetime.date.today().year
    if val > current_year:
        raise ValidationError('Такой год еще не наступил')

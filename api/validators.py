import re

from django.conf import settings
from django.core.exceptions import ValidationError


def regex_check_number(number):
    """Проверка валидности номера телефона"""
    pattern = r'^[+]?[0-9]{10,13}$'
    match = re.fullmatch(pattern, re.sub(r'\s|\(|\)|-', '', number))
    if not match:
        raise ValidationError('Некорректный номер телефона.')
    if match.string.startswith('+'):
        return match.string
    return f'+{match.string}'


def validate_name(value):
    """Проверка валидности имени и фамилии"""
    if len(value) < settings.NAMES_MIN_LENGTH:
        raise ValidationError(
            f'Имя и Фамилия должны быть не менее {settings.NAMES_MIN_LENGTH} '
            'символов.'
        )
    pattern = r'^[a-zA-Z\u0400-\u04FF-]+$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Имя и Фамилия должны состоять только из букв и символа -.'
        )
    return value

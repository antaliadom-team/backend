from django.core.exceptions import ValidationError
import re


def regex_check_number(number):
    """Проверка валидности номера телефона"""
    pattern = r'^[+]?[0-9]{10,13}$'
    match = re.fullmatch(pattern, re.sub(r'\s|\(|\)|-', '', number))
    if not match:
        raise ValidationError('Некорректный номер')
    if match.string.startswith('+'):
        return match.string
    return f'+{match.string}'

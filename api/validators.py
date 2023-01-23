from django.core.exceptions import ValidationError
import re


def phone_number_validator(self, value):
    """
    Проверяет длину номера телефона и добавляет знак '+',
    если он отсутстует.
    """
    if value[0] == '+':
        if len(value) < 12:
            raise ValidationError('Номер слишком короткий!')
        self._number_check(value=value, start=1)
    else:
        if len(value) < 10:
            raise ValidationError('Номер слишком короткий!')
        self._number_check(value=value, start=0)
        return '+' + value
    return value


def _number_check(self, value, start):
    """Проверяет чтоб номер телефона состоял из цифр."""
    for i in range(start, len(value)):
        try:
            int(value[i])
        except ValueError:
            raise ValidationError('Номер телефона должен состоять из чисел.')


def regex_check_number(number): #возможно одна проверка будет удобнее
    """Проверка валидности номера телефона"""
    pattern = (
        r'[+]?[0-9]?[\(-]?[0-9]{3}[\)-]?[-]?[0-9]{3}[-]?[0-9]{2}[-]?[0-9]{2}')
    match = re.fullmatch(pattern, number)
    if not match:
        raise ValidationError('Некорректный номер')
    return '+' + re.sub(r'[+\(\)-]', '', match.string)

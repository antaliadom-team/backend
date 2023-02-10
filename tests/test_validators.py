from django.core.exceptions import ValidationError

import pytest

from api.validators import regex_check_number, validate_name


class TestValidators:
    @pytest.mark.parametrize('wrong_number', ['+1abcd3345', '123456789012345'])
    def test_wrong_number_validator(self, wrong_number):
        with pytest.raises(ValidationError):
            assert (
                regex_check_number(wrong_number) == False
            ), f'Ошибка в работе валидатора на номер {wrong_number}'

    @pytest.mark.parametrize('right_number', ['+901234567890', '+79876543210'])
    def test_right_number_validator(self, right_number):
        validated_number = regex_check_number(right_number)
        assert (
            validated_number == right_number
        ), f'Ошибка в возвращаемом значении {validated_number} валидатора'

    def test_right_number_without_plus_sign(self):
        right_number = '901234567890'
        assert (
            regex_check_number(right_number) == f'+{right_number}'
        ), f'Ошибка в возвращаемом значении {right_number} валидатора'

    @pytest.mark.parametrize(
        'number_with_delimeters',
        [
            '+7(123)4567890',
            '+7 123 456 78 90',
            '+7-123-456-78-90',
            '7 (123) 456-78-90',
        ],
    )
    def test_number_with_delimeters(self, number_with_delimeters):
        assert regex_check_number(number_with_delimeters) == '+71234567890', (
            f'Ошибка в возвращаемом значении '
            f'{number_with_delimeters} валидатора'
        )

    def test_validate_name_success(self):
        assert (
            validate_name('Иван') == 'Иван'
        ), 'Ошибка в возвращаемом значении валидатора'
        assert (
            validate_name('Иван-Иван') == 'Иван-Иван'
        ), 'Ошибка в возвращаемом значении валидатора. Должен пропускать -'

    @pytest.mark.parametrize(
        'wrong_names',
        [
            'Иван1',
            'Иван-Иван1',
            'Иван Иван',
            '111',
            'Иван"№;%:?*()_+',
        ],
    )
    def test_validate_name_wrong(self, wrong_names):
        with pytest.raises(ValidationError):
            assert (
                validate_name(wrong_names) == False
            ), f'Ошибка в работе валидатора на Имя {wrong_names}'
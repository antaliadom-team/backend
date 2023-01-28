import pytest
from django.core.exceptions import ValidationError

from api.validators import regex_check_number


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

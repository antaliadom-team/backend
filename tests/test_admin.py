import pytest

from catalog.admin import RealEstateAdmin


@pytest.mark.django_db
class TestAdminSite:
    """Тест администраторской части проекта"""

    def test_favorites_count(self, object1):
        assert (
            RealEstateAdmin.price_with_currency(self, object1)
            == f'{object1.price}{object1.currency} в {object1.period}'
        ), 'Вывод цены, валюты и периода не соответствует ожидаемому'

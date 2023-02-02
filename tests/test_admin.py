import pytest

from catalog.admin import RealEstateAdmin


@pytest.mark.django_db
class TestAdminSite:
    """Тест администраторской части проекта"""

    def test_price_and_period_field_rent(self, object1):
        assert (
            RealEstateAdmin.price_with_currency(self, object1)
            == f'{object1.price}{object1.currency} в {object1.period.lower()}'
        ), 'Вывод цены, валюты и периода не соответствует ожидаемому'

    def test_price_and_period_field_sell(self, object2):
        assert (
            RealEstateAdmin.price_with_currency(self, object2)
            == f'{object2.price}{object2.currency}'
        ), 'Вывод цены, валюты и периода не соответствует ожидаемому'
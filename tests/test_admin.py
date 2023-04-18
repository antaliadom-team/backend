import pytest

from catalog.admin import RealEstateAdmin
from core.utils import AdminImageWidget


@pytest.mark.django_db
class TestAdminSite:
    """Тест администраторской части проекта"""

    def test_price_and_period_field_rent(self, object2):
        assert (
            RealEstateAdmin.price_with_currency(self, object2)
            == f'{object2.price}{object2.currency} в {object2.period.lower()}'
        ), 'Вывод цены, валюты и периода не соответствует ожидаемому'

    def test_price_and_period_field_sell(self, object1):
        assert (
            RealEstateAdmin.price_with_currency(self, object1)
            == f'{object1.price}{object1.currency}'
        ), 'Вывод цены, валюты и периода не соответствует ожидаемому'

    def test_render_image_widget(self, image_file):
        # Instantiate the widget with a name and value
        widget = AdminImageWidget()
        name = 'test_image'

        # Render the widget HTML markup
        rendered = widget.render(name, image_file)

        # Check if the rendered output includes the expected HTML markup
        assert '<a href="' in rendered
        assert 'target="_blank"><img src="' in rendered
        assert 'style="object-fit: cover;"/></a>' in rendered
        assert 'test_image.jpg' in rendered

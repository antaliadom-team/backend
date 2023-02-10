from django.contrib.auth import get_user_model

from common import APITestBase
import pytest

from catalog.models import Favorite

User = get_user_model()


@pytest.mark.django_db(transaction=True)
class TestAPI(APITestBase):
    """Test API"""

    def test_favorite_object(self, user_client, favorite):
        """Test add object to favorites"""

        url = self.urls['favorite'].format(object_id=favorite.real_estate.id)
        wrong_recipe_url = self.urls['favorite'].format(object_id=999999999)

        # Get method not allowed
        self.assert_status_code(405, user_client.get(url), url=url)
        # POST of non-existent object
        self.assert_status_code(
            404, user_client.post(wrong_recipe_url), url=wrong_recipe_url
        )
        # Delete the object from favorites
        self.assert_status_code(204, user_client.delete(url), url=url)
        assert (
            Favorite.objects.count() == 0
        ), 'Объект должен быть удален из избранного'

        # Add the object to favorites
        self.assert_status_code(201, user_client.post(url), url=url)

        # Add same recipe twice cause 400 error
        self.assert_status_code(400, user_client.post(url), url=url)
        assert Favorite.objects.count() == 1, 'Объект должен быть добавлен'

        # Delete non-existent object from favorites
        Favorite.objects.all().delete()
        self.assert_status_code(400, user_client.delete(url), url=url)


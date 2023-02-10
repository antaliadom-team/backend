import pytest

from common import APITestBase


class TestURLs(APITestBase):
    """Test URLs"""

    def test_urls_anonymous_user(
        self, client, user, object1, facility1, static_page, team_member1
    ):
        """Test URLs available for any user"""
        for url in self.urls.values():
            try:
                url = url.format(
                    user_id=user.id,
                    object_id=object1.id,
                    property_type_id=object1.property_type.id,
                    location_id=object1.location.slug,
                    facility_id=facility1.id,
                    category_id=object1.category.id,
                    static_id=static_page.id,
                    member_id=team_member1.id,
                )
            except KeyError:
                pass
            try:
                response = client.get(url)
            except Exception as e:
                assert False, f'При запросе на `{url}` возникла ошибка: {e}'
            assert (
                response.status_code != 404
            ), f'Адрес {url} не найден, проверьте этот адрес в urls.py'

    @pytest.mark.parametrize(
        'disabled_endpoints',
        [
            'resend_activation/',
            'activation/',
            'reset_password/',
            'reset_username/',
            'set_username/',
            'reset_password_confirm/',
            'reset_username_confirm/',
        ],
    )
    def test_disabled_joser_endpoints(self, user_client, disabled_endpoints):
        """Disabled djoser's endpoints should return 404s"""
        full_url = '/api/users/' + disabled_endpoints
        self.assert_status_code(
            404, user_client.get(full_url), url=full_url
        )

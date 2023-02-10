class APITestBase:
    urls = {
        # Users
        'users': '/api/users/',
        'users_detail': '/api/users/{user_id}/',
        'users_me': '/api/users/me/',
        'set_password': '/api/users/set_password/',
        'users_logout': '/api/users/logout/',
        # Auth
        'get_token': '/api/auth/jwt/create/',
        'refresh_token': '/api/auth/jwt/refresh/',
        'verify_token': '/api/auth/jwt/verify/',
        # 'logout': '/api/auth/jwt/logout/',
        # Real Estate
        'real_estate_list': '/api/objects/',
        'real_estate_detail': '/api/objects/{object_id}/',
        # Real Estate Types
        'real_estate_type_list': '/api/objects/property_types/',
        'real_estate_type_detail': '/api/objects/property_types/{property_type_id}/',
        # Real Estate Locations
        'location_list': '/api/objects/locations/',
        'location_detail': '/api/objects/locations/{location_id}/',
        # Real Estate Facilities
        'facility_list': '/api/objects/facilities/',
        'facility_detail': '/api/objects/facilities/{facility_id}/',
        # Real Estate Categories
        'category_list': '/api/objects/categories/',
        'category_detail': '/api/objects/categories/{category_id}/',
        # Orders
        'order_general': '/api/objects/order/',
        'real_estate_order': '/api/objects/{object_id}/order/',
        # Favorite objects
        'favorite': '/api/objects/{object_id}/favorite/',
        # Static pages
        'static_page_list': '/api/static_pages/',
        'static_page': '/api/static_pages/{static_id}/',
        'team': '/api/static_pages/team/',
        'team_member': '/api/static_pages/team/{member_id}/',
    }

    def assert_fields(self, fields_required, response, *args, **kwargs):
        """Assertion to check fields in response"""
        url = kwargs.get('url')
        if isinstance(response, list):
            response_data = response[0].keys()
        else:
            response_data = response.json().keys()
        for field in fields_required:
            assert field in response_data, (
                f'При запросе на `{url}` должны возвращаться '
                f'{fields_required} поля. В ответе не найдено поле {field}'
            )
        return response

    def assert_status_code(self, code_expected, response, *args, **kwargs):
        """Assertion to check status code in response"""
        url = kwargs.get('url')
        response_data = ''
        try:
            response_data = response.json()
        # if no data in answer at all
        except TypeError:
            pass
        # if content-type not a json
        except ValueError:
            pass
        assert response.status_code == code_expected, (
            f'При запросе `{url}` со всеми параметрами должен возвращаться '
            f'код {code_expected}, а вернулся код {response.status_code}:'
            f' {response_data}'
        )
        return response

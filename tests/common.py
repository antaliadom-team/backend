class APITestBase:
    urls = {
        # Users
        'users': '/api/users/',
        'users_detail': '/api/users/{user_id}/',
        'users_me': '/api/users/me/',
        'set_password': '/api/users/set_password/',
        'reset_password': '/api/users/reset_password/',
        'reset_password_confirm': '/api/users/reset_password_confirm/',

        # TODO: уточнить после того, как определимся какие будут токены
        'get_token': '/api/auth/token/login/',
        'delete_token': '/api/auth/token/logout/',
        # Objects
        'object_list': '/api/catalog/',
        'object_detail': '/api/catalog/{object_id}/',
        # Requests
        'buyer_request': '/api/catalog/requests/',
        'object_to_request': '/api/catalog/{object_id}/request/',
        # Favorites
        'favorites': '/api/catalog/{object_id}/favorite/',
        # Static pages
        'static_page_list': '/api/static_pages/',
        'static_page': '/api/static_pages/{slug}/',
        'team': '/api/static_pages/team/',
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

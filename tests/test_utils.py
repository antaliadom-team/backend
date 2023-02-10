from django.core import mail


class TestCoreUtils:
    """Тесты для core.utils"""

    def test_send_common_order_emails_anon(self, admin, object1):
        """Test send_order_emails function for anonymous user"""
        # Test uses settings fixture from fixtures/fixture_conf.py
        # for changing email backend to locmem
        from core.utils import send_order_emails

        data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'ivan@mail.fake',
            'phone': '+79999999999',
            'category': object1.category,
            'location': object1.location,
            'property_type': object1.property_type,
            'rooms': 1,
            'comment': 'comment',
            'agreement': True,
            'date_added': '2021-02-01',
        }
        send_order_emails(data)

        assert len(mail.outbox) == 2
        assert mail.outbox[0].subject == 'Подтверждение заявки.'
        assert mail.outbox[1].subject == 'Поступила новая заявка.'

    def test_send_common_order_emails_user(self, user, admin, object1):
        """Test send_order_emails function for authenticated user"""
        from core.utils import send_order_emails

        data = {
            'category': object1.category,
            'location': object1.location,
            'property_type': object1.property_type,
            'rooms': 1,
            'comment': 'comment',
            'agreement': True,
            'date_added': '2021-02-01',
        }
        send_order_emails(data, user=user)

        assert len(mail.outbox) == 2
        assert mail.outbox[0].subject == 'Подтверждение заявки.'
        assert mail.outbox[1].subject == 'Поступила новая заявка.'

    def test_send_reale_state_order_emails_user_anon(self, admin, object1):
        """Test send_order_emails function for anonymous user"""
        from core.utils import send_order_emails

        data = {
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'email': 'ivan@mail.fake',
            'phone': '+79999999999',
            'comment': 'comment',
            'agreement': True,
            'category': object1.category,
            'location': object1.location,
            'property_type': object1.property_type,
            'rooms': object1.rooms,
            'date_added': '2021-02-01',
        }
        send_order_emails(data, real_estate=object1)
        assert len(mail.outbox) == 2
        assert mail.outbox[0].subject == 'Подтверждение заявки.'
        assert mail.outbox[1].subject == 'Поступила новая заявка.'

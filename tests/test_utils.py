from django.core import mail


class TestCoreUtils:
    """Тесты для core.utils"""

    def test_send_order_emails(self):
        """TODO: дописать тесты для функции send_order_emails"""
        mail.send_mail(
            'subject', 'body.', 'from@example.com', ['to@example.com']
        )
        assert len(mail.outbox) == 1

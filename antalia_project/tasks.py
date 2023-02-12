from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from celery import shared_task

from catalog.models import RealEstate

User = get_user_model()


def format_real_estate_message(real_estate):
    """Форматирует сообщение для объекта недвижимости"""
    return (
        f'Заявка по объекту недвижимости #{real_estate.id} - '
        f'{real_estate.title} <link>'
    )


@shared_task
def send_order_emails(data, user_id=None, *args, **kwargs):
    """Отправляет уведомление клиенту на почту о приеме заявки и рассылает
    уведомление на почту администраторам о поступлении заявки"""

    # Получение списка адресов администраторов
    admins = (
        User.objects.filter(is_staff=True)
        .values_list('email', flat=True)
        .distinct()
    )
    # Если пользователь авторизован, то получаем его данные
    if user_id is not None:
        user = User.objects.get(pk=user_id)
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['email'] = user.email
        data['phone'] = user.phone
    # Если это заявка на объект, то формируем дополнительное сообщение
    if 'real_estate_id' in kwargs:
        real_estate_message = format_real_estate_message(
            RealEstate.objects.get(id=kwargs['real_estate_id'])
        )
    else:
        real_estate_message = ''
    # Формирование сообщений
    message_to_user = settings.EMAIL_USER_MESSAGE.format(**data)
    message_to_admins = settings.EMAIL_ADMIN_MESSAGE.format(**data)
    # Отправка почты пользователю
    send_mail(
        subject=settings.EMAIL_USER_SUBJECT,
        message=message_to_user + real_estate_message,
        # html_message=settings.EMAIL_HTML_MESSAGE_USER,
        from_email=settings.EMAIL_REPLY_TO,
        recipient_list=(data['email'],),
    )
    # Отправка почты админам
    send_mail(
        subject=settings.EMAIL_ADMIN_SUBJECT,
        message=message_to_admins + real_estate_message,
        # html_message=settings.EMAIL_HTML_MESSAGE_ADMIN,
        from_email=settings.EMAIL_REPLY_TO,
        recipient_list=admins,
    )

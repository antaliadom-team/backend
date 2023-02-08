from django.conf import settings
from django.contrib.admin.widgets import AdminFileWidget
from django.contrib.auth.models import AnonymousUser
from django.core import mail
from django.utils.safestring import mark_safe

from users.models import User


class AdminImageWidget(AdminFileWidget):
    """Поле для картинки в админке с превьюшкой"""

    def render(self, name, value, attrs=None, **kwargs):
        output = []
        if value and getattr(value, 'url', None):
            image_url = value.url
            file_name = str(value)
            output.append(
                f'<a href="{image_url}" target="_blank"><img src="{image_url}"'
                f'alt="{file_name}" width="200" height="200" '
                f'style="object-fit: cover;"/></a> '.format(
                    image_url=image_url, file_name=file_name
                )
            )
        output.append(super().render(name, value, attrs, **kwargs))
        return mark_safe("".join(output))


def format_real_estate_message(real_estate):
    """Форматирует сообщение для объекта недвижимости"""
    return (
        f'Заявка по объекту недвижимости #{real_estate.id} - '
        f'{real_estate.title} <link>'
    )


def send_order_emails(data, user=AnonymousUser, *args, **kwargs):
    """Отправляет уведомление клиенту на почту о приеме заявки и рассылает
    уведомление на почту администраторам о поступлении заявки"""

    # Если есть объект недвижимости, сохраняем его в переменную, иначе None
    admins = (
        User.objects.filter(is_staff=True)
        .values_list('email', flat=True)
        .distinct()
    )
    # Если пользователь авторизован, то берем данные из объекта юзера, иначе из
    # сериализатора
    if user.is_authenticated:
        data['first_name'] = user.first_name
        data['last_name'] = user.last_name
        data['email'] = user.email
        data['phone'] = user.phone

    # Формирование сообщений
    message_to_user = settings.EMAIL_USER_MESSAGE.format(**data)
    message_to_admins = settings.EMAIL_ADMIN_MESSAGE.format(**data)
    # Если это заявка на объект, то в сообщение добавляется ссылка на него
    if kwargs.get('real_estate'):
        message_to_user += format_real_estate_message(kwargs['real_estate'])
        message_to_admins += format_real_estate_message(kwargs['real_estate'])

    # Отправка почты пользователю
    mail.send_mail(
        subject=settings.EMAIL_USER_SUBJECT,
        message=message_to_user,
        # html_message=settings.EMAIL_HTML_MESSAGE_USER,
        from_email=settings.EMAIL_REPLY_TO,
        recipient_list=(data['email'],),
    )
    # Отправка почты админам
    mail.send_mail(
        subject=settings.EMAIL_ADMIN_SUBJECT,
        message=message_to_admins,
        # html_message=settings.EMAIL_HTML_MESSAGE_ADMIN,
        from_email=settings.EMAIL_REPLY_TO,
        recipient_list=admins,
    )

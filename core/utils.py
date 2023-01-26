from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from users.models import User
from django.core import mail
from django.conf import settings


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
        return mark_safe(u''.join(output))


def send_order_emails(user):
    """Отправляет уведомление клиенту по почту о приеме заявки и рассылает
     уведомление на почту адинастраторам о поступлении заявки"""
    mail.send_mail(
        subject='Подтверждение заявки.',
        message=settings.EMAIL_USER_MESSAGE.format(
            user_full_name=user.get_full_name()
        ),
        html_message=settings.EMAIL_HTML_MESSAGE_USER,
        from_email=settings.EMAIL_REPLY_TO,
        recipient_list=(user.email,),
    )
    for admin in (
        User.objects.filter(is_staff=True)
        .values('first_name', 'last_name', 'email')
        .distinct()
    ):
        mail.send_mail(
            subject='Новая заявка.',
            message=settings.EMAIL_ADMIN_MESSAGE.format(
                admin_full_name=user.get_full_name()
            ),
            html_message=settings.EMAIL_HTML_MESSAGE_ADMIN,
            from_email=settings.EMAIL_REPLY_TO,
            recipient_list=(admin['email'],),
        )

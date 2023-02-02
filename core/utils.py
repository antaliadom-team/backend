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


def send_order_emails(user, data):
    """Отправляет уведомление клиенту на почту о приеме заявки и рассылает
     уведомление на почту администраторам о поступлении заявки"""
    admins = User.objects.filter(is_staff=True).values('email').distinct()
    unauthorized_user_data = {
        'user_full_name': f"{data['first_name']} {data['last_name']}",
        'first_name': data['first_name'],
        'last_name': data['last_name']}
    authorized_user_data = {
        'user_full_name': user.get_full_name(),
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email}
    data = {
        'category': data['category'],
        'location': data['location'],
        'property_type': data['property_type'],
        'rooms': data['rooms'],
        'phone_number': data['phone_number'],
        'email': data['email'],
        'date_added': data['date_added'],
        'comment': data['comment']}
    mail.send_mail(
        subject='Подтверждение заявки.',
        message=settings.EMAIL_USER_MESSAGE.format(
            {**unauthorized_user_data, **data}) if user is None else
        settings.EMAIL_USER_MESSAGE.format(
            {**authorized_user_data, **data}),
        html_message=settings.EMAIL_HTML_MESSAGE_USER,
        from_email=settings.EMAIL_REPLY_TO,
        recipient_list=(data['email'],),)
    mail.send_mail(
        subject='Новая заявка.',
        message=settings.EMAIL_ADMIN_MESSAGE.format(
            {**unauthorized_user_data, **data}) if user is None else
        settings.EMAIL_ADMIN_MESSAGE.format(
            {**authorized_user_data, **data}),
        html_message=settings.EMAIL_HTML_MESSAGE_ADMIN,
        from_email=settings.EMAIL_REPLY_TO,
        recipient_list=admins,)

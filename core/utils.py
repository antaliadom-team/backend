from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe
from users.models import User
from django.core import mail

class AdminImageWidget(AdminFileWidget):
    """Поле для картинки в админке с превьюшкой"""
    def render(self, name, value, attrs=None, **kwargs):
        output = []
        if value and getattr(value, 'url', None):
            image_url = value.url
            file_name = str(value)
            output.append(
                f' <a href="{image_url}" target="_blank"><img src="{image_url}"'
                f'alt="{file_name}" width="200" height="200" '
                f'style="object-fit: cover;"/></a> '.format(
                    image_url=image_url, file_name=file_name
                )
            )
        output.append(super().render(name, value, attrs, **kwargs))
        return mark_safe(u''.join(output))


def send_order_emails(user):
    mail.send_mail(subject='Подтверждение заявки.',
                   message=f'Здравствуйте {user.get_full_name()}.'
                           f' Ваша заявка была принята в работу, '
                           f'скоро с вами свяжется сотрудник нашего агентства.',
                   from_email='antalyadom@telfia.com',
                   recipient_list=(user.email,))
    for admin in User.objects.filter(is_staff=True).values(
            'first_name', 'last_name', 'email').distinct():
        mail.send_mail(subject='Новая заявка.',
                       message=f'Поступила заявка от {user.get_full_name()}.',
                       from_email='antalyadom@telfia.com',
                       recipient_list=(admin['email'],))

from django.contrib.admin.widgets import AdminFileWidget
from django.utils.safestring import mark_safe

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
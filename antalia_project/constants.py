# константы для отправки электронных писем
EMAIL_USER_SUBJECT = 'Подтверждение заявки.'
EMAIL_ADMIN_SUBJECT = 'Поступила новая заявка.'
EMAIL_ADMIN_MESSAGE = (
    'Поступила заявка от {first_name} {last_name}.\n\n'
    'Были предоставлены следующие данные:\n'
    'Имя: {first_name}\n'
    'Фамилия: {last_name}\n'
    'Электронная почта: {email}\n'
    'Номер для связи: {phone}\n\n'
    'Тип сделки: {category}\n'
    'Локация: {location}\n'
    'Тип недвижимости: {property_type}\n'
    'Количество комнат: {rooms}\n\n'
    'Комментарий: {comment}\n\n'
    'Дата подачи заявки: {date_added}'
)
EMAIL_USER_MESSAGE = (
    'Здравствуйте, {first_name}. Ваша заявка была принята в работу,'
    'скоро с вами свяжется сотрудник нашего агентства.\n\n'
    'По вашей заявке были приняты следующие данные:\n'
    'Имя: {first_name}\n'
    'Фамилия: {last_name}\n'
    'Электронная почта: {email}\n'
    'Номер для связи: {phone}\n\n'
    'Тип сделки: {category}\n'
    'Локация: {location}\n'
    'Тип недвижимости: {property_type}\n'
    'Количество комнат: {rooms}\n'
    'Комментарий: {comment}\n\n'
    'Дата подачи заявки: {date_added}'
)
EMAIL_HTML_MESSAGE_ADMIN = ''  # можно прикрутить HTML
EMAIL_HTML_MESSAGE_USER = ''  # можно прикрутить HTML

NA = 'Не указано'

# Константы для моделей
EMAIL_LENGTH = 50
USER_ROLE_LENGTH = 6
PHONE_LENGTH = 14
NAMES_LENGTH = 30
LONG_NAMES_LENGTH = 100
ESTATE_TITLE_LENGTH = 200
SLUG_LENGTH = 100
LONG_SLUG_LENGTH = 255
PROPERTY_MAX_LENGTH = 50
ICON_SLUG = 100
COMMENT_LENGTH = 200
CONF_CODE_LENGTH = 32
PASSWORD_LENGTH = 128
IMAGE_LIMIT = 6

# константы проекта
ROOMS_LIMIT = 4

# Список размеров в пикселях создаваемых превью для фотографий объекта [(hor, vert), ...]
PREVIEW_SIZES = ((738, 632), (328, 261))

# константы для отправки электронных писем
EMAIL_REPLY_TO = 'antalyadom@telfia.com'
EMAIL_ADMIN_MESSAGE = (
    'Поступила заявка от {user_full_name}.'
    'Были предоставлены следующие данные:'
    'Имя: {first_name}'
    'Фамилия: {last_name}'
    'Электронная почта: {email}'
    'Тип сделки: {category}'
    'Локация: {location}'
    'Тип недвижимости: {property_type}'
    'Количество комнат: {rooms}'
    'Номер для связи: {phone_number}'
    'Дата подачи заявки: {date_added}'
    'Комментарий: {comment}'
)
EMAIL_USER_MESSAGE = (
    'Здравствуйте {user_full_name}. Ваша заявка была принята в работу,'
    'скоро с вами свяжется сотрудник нашего агентства.'
    'По вашей заявке были приняты следующие данные:'
    'Имя: {first_name}'
    'Фамилия: {last_name}'
    'Электронная почта: {email}'
    'Тип сделки: {category}'
    'Локация: {location}'
    'Тип недвижимости: {property_type}'
    'Количество комнат: {rooms}'
    'Номер для связи: {phone_number}'
    'Дата подачи заявки: {date_added}'
    'Комментарий: {comment}'
)
EMAIL_HTML_MESSAGE_ADMIN = ''  # можно прикрутить HTML
EMAIL_HTML_MESSAGE_USER = ''  # можно прикрутить HTML

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

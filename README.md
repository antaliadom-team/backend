![ci workflow](https://github.com/antaliadom-team/backend/actions/workflows/tests_deploy.yaml/badge.svg) [![codecov](https://codecov.io/github/antaliadom-team/backend/branch/dev/graph/badge.svg?token=IS5MLKDVWZ)](https://codecov.io/github/antaliadom-team/backend) ![Django](https://img.shields.io/badge/Django-3.2.16-green) ![DRF](https://img.shields.io/badge/DRF-3.12.4-green)

<br>
<p align="center">
  <img alt="AntalyaDom" title="AntalyaDom" src="http://antalyadom.telfia.com/static/media/logo.2135c2d77e78f750e72f2587315aacff.svg" width="650">
</p>
<br>

## Бэкэнд проекта "Анталия Дом"

`Анталия Дом` - сайт агенства недвижимости. Бэкенд проекта представляет собой RESTful API, позволяющий регистрироваться новым пользователям, получать доступ к объектам недвижимости, добавлять объекты в избранное, оставлять заявку на подбор объекта недвижимости или заявку на понравившейся объект. Заявки отправляются по емейлу пользователю и администраторам. Помимо этого, бэкенд выдает некоторые статические страницы, например, информацию о команде проекта.

Для проекта написан ci/cd пайплайн с автоматической проверкой форматирования кода при открытии пул-реквестов, автоматическим тестированием при мерже в основую ветку разработки и деплоем на тестовый сервер. Дополнительно происходит автоматический деплой документации API при изменениях.


## Содержание

- [Документация к проекту](#документация-к-проекту)
- [Как приступить к разработке?](#как-приступить-к-разработке)
- [Несколько требований к проекту](#несколько-требований-к-проекту)
- [Использованные технологии](#%использованные-технологии)
- [Тестирование](https://github.com/antaliadom-team/backend/blob/dev/tests/README.md)
- [Авторы](#авторы)

## Документация к проекту

 - [Описание моделей, диаграмма](https://dbdiagram.io/d/63a97dc77d39e42284e788a0)
 - [Документация к API](http://antalyadom.telfia.com/api/docs/)

<p align="right"><a href="#top">⬆️ Наверх</a></p>

## Как приступить к разработке?

  1. Клонировать репозиторий `git clone https://github.com/antaliadom-team/backend.git`
  2. Перейти в папку с проектом  `cd backend`
  3. Создать и активировать виртуальное окружение
     ```
     python -m venv .venv
     source env/bin/activate
     ```
  4. Установить зависимости
     ```
     python -m pip install --upgrade pip
     pip install -r requirements.txt
     ```
  5. В папке backend cоздать файл .env по шаблону:
     ```
     EMAIL_HOST_USER=antalyadom@telfia.com
     EMAIL_HOST_PASSWORD=<Пароль спрашивайте в дискорде>
     SECRET_KEY=some-random-secret-django-key
     ALLOWED_HOSTS="127.0.0.1 localhost backend"
     DEBUG=True
     CORS_WHITELIST="http://localhost:3000 http://localhost:8080"
     ```
  5. Применить миграции
     ```
     python manage.py migrate
     ```
  6. Опционально: В отдельном терминале запустить воркер celery (требуется также Redis)
     ```
     celery -A antalia_project worker -l info -B
     ```
  6.1. Для Windows у celery есть специальный костыль.
  ```
  celery -A your-application worker -l info --pool=solo
  ```
  6. Перейти в ветку разраработки `git checkout dev`
  7. Из ветки `dev` создать и перейти в ветку с названием вашей работы `git checkout -b feature/api`
  8. Запушить изменения с коммитом "добавляет эндпоинт каталога"
  9. Радоваться что всё прошло успешно :tada:

<p align="right"><a href="#top">⬆️ Наверх</a></p>

## Несколько требований к проекту

  - Оформляем код по [PEP8](https://peps.python.org/pep-0008/)
  - Форматируем код black с настройкой `--line-length=79 --skip-string-normalization`, isort
  - Кавычки везде, где применимо одинарные
  - Все классы и основные функции документируем хотя бы в 1 строку: `"""Модель юзеров"""`
  - Используем линтер flake8 (перед PR обязательно)
  - Для именования запрещены транслит, сокращения, названия переменных, приложений, урлов и т.д. должны быть переведены на английский
  - Константы выносим на уровень модуля, пишем заглавными буквами, если уместно, выносим в settings.py
  - Код оформлен по принципам программирования DRY:droplet:(не повторяй сам себя) и KISS:kiss:(пиши проще и понятней)

<p align="right"><a href="#top">⬆️ Наверх</a></p>

## Пару слов о том как работать с git

 - Проект содержит основую ветку `main`. Она предназначена для релизного состояния приложения
 - Ветка `dev` предназначена для слияния наших работ
 - Для того чтобы смержить изменения в ветку `dev` необходимо из этой ветки создать ветку с вашей работой и создать пул реквест
 - Название вашей рабочей ветки должно отражать вашу работу. Например `feature/api-users` или `feature/models`
 - Коммиты пишем на русском языке. Начинается коммит с глагола, отвечающий на вопрос "что будет, если этот коммит слить с остальным кодом?" Например, "фиксит пермишины" или "добавляет тесты эндпоинта юзеров"
 - Если пул реквест принят ветка в которой велась разработка удаляется
 - [Подробнее о git-flow](https://github.com/SergeFocus/git-flow)

<p align="right"><a href="#top">⬆️ Наверх</a></p>

## Использованные технологии

 - Python 3.8
 - Django 3.2.16
 - Django Rest Framework
 - Pytest
 - FactoryBoy
 - Celery
 - Redis
 - Docker

## Авторы:

 - [Роман](https://github.com/spaut33)
 - [Дмитрий](https://github.com/kultmet)
 - [Павел](https://github.com/pencool)

 <p align="right"><a href="#top">⬆️ Наверх</a></p>

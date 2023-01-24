# Бэкэнд проекта Анталия Дом 🏡

## Над проектом трудятся:

 - [Роман](https://github.com/spaut33)
 - [Дмитрий](https://github.com/kultmet)
 - [Павел](https://github.com/pencool)
 
## Используемые технологии

 - Python 3.8
 - Django 3.2.16
 - Django Rest Framework
 - Djoser

## Диаграмма и описание моделей

 - https://dbdiagram.io/d/63a97dc77d39e42284e788a0

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
  6. Перейти в ветку разраработки `git checkout dev`
  7. Из ветки `dev` создать и перейти в ветку с названием вашей работы `git checkout -b feature/api-catalog`
  8. Запушить изменения с коммитом "добавляет эндпоинт каталога"
  9. Радоваться что всё прошло успешно :tada:

## Несколько требований к проекту

  - Оформляем код по [PEP8](https://peps.python.org/pep-0008/)
  - Форматируем код black с настройкой `--line-length=79 --skip-string-normalization`, isort
  - Кавычки везде, где применимо одинарные
  - Все классы и основные функции документируем хотя бы в 1 строку: `"""Модель юзеров"""`
  - Используем линтер flake8 (перед PR обязательно)
  - Для именования запрещены транслит, сокращения, названия переменных, приложений, урлов и т.д. должны быть переведены на английский
  - Константы выносим на уровень модуля, пишем заглавными буквами, если уместно, выносим в settings.py
  - Код оформлен по принципам программирования DRY:droplet:(не повторяй сам себя) и KISS:kiss:(пиши проще и понятней)


## Пару слов о том как работать с git

 - Проект содержит основую ветку `main`. Она предназначена для релизного состояния приложения
 - Ветка `dev` предназначена для слияния наших работ
 - Для того чтобы смержить изменения в ветку `dev` необходимо из этой ветки создать ветку с вашей работой и создать пул реквест
 - Название вашей рабочей ветки должно отражать вашу работу. Например `feature/api-users` или `feature/models`
 - Коммиты пишем на русском языке. Начинается коммит с глагола, отвечающий на вопрос "что будет, если этот коммит слить с остальным кодом?" Например, "фиксит пермишины" или "добавляет тесты эндпоинта юзеров"
 - Если пул реквест принят ветка в которой велась разработка удаляется
 - [Подробнее о git-flow](https://github.com/SergeFocus/git-flow)
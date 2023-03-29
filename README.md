[![API_yamdb deployy latest](https://github.com/platonov1727/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/platonov1727/yamdb_final/actions/workflows/yamdb_workflow.yml)

# Yamdb_final

Финальный проект 16 спринта YaP

## Описание

Сервис Апи для того, чтобы собирать пользовательские оценки и комментарии на произведения различных категорий и жанров.

## Подробная документация по адресу YOURHOST/redoc/

В redoc описанны все ендпоинты и их возможности с примерами запросов. И ожидаемые ответы.

## Возможности

- JWT Аутентификация
- возможность ознакомиться с отзывами без аутентификации(но нельзя оставить отзыв и поставить оценку)
- Получение списка всех категорий и жанров, добавление и удаление.
- Пользователи могут самостоятельно зарегистрироваться через идентификацию по email
- Есть возможность назначить администратора, модератора

## Технологии

- Django==3.2
- django-filter==22.1
- django-import-export==3.0.2
- djangorestframework==3.12.4
- djangorestframework-simplejwt==5.2.2
- PyJWT==2.1.0

со списком всех используемых библиотек можно ознакомиться в файлe requirements.txt

## Инструкции по развертыванию проекта в dev режиме

## Запуск проекта в dev-режиме

``` code
git clone <название репозитория>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
Load test data in django admin panel
python manage.py runserver
```

## Инструкции по развертыванию проекта в docker

- Установите Docker, используя инструкции с официального сайта.
- Склонируйте репозиторий на локальную машину

```code
git clone git@github.com:platonov1727/yamdb_final.git
```

- Создайте файл .env командой

``` code
touch .env
```

- Добавьте в него переменные окружения для работы с базой данных:

```python
ENGINE ='django.db.backends.postgresql'
DB_NAME=postgres # имя базы данных
POSTGRES_USER=postgres # логин для подключения к базе данных
POSTGRES_PASSWORD=postgres # пароль для подключения к БД (установите свой)
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД 
```

- Запустите docker-compose командой

``` code
sudo docker-compose up -d
```

- Выполните миграции

```code
sudo docker-compose exec yamdb python manage.py migrate
```

- Соберите статику командой

```code
sudo docker-compose exec yamdb python manage.py collectstatic --no-input
```

- Создайте суперпользователя Django

```code
sudo docker-compose exec yamdb python manage.py createsuperuser --username admin --email 'admin@yamdb.com'
```

# Авторы

https://github.com/Shabanov010 - Шабанов Дмитрий

https://github.com/platonov1727 - Платонов Сергей

https://github.com/mariarozhina - Рожина Мария

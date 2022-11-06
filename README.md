## Hasker: Poor Man's Stackoverflow
Q&A сайт аналог Stackoverflow

## Стек:
 - Django 
 - PostgreSQL
 - RabbitMQ + AioPika
 - Docker-Compose
 - NGINX + uWSGI

## Команды для запуска:
 - make prod - создаёт билд
 - make migrate - применяет миграции
 - make worker - запуск воркера для RabbitMQ
 - make down - остановка контейнеров
 - make test - выполнить тесты

## Для работы нужно создать ENV файл с параметрами:
```
SECRET_KEY = "django-insecure-)!4&s=n4zo6#n_jae5&4o(l8zy*mn3hr9+(z$kdm43@8p@u7#o"

POSTGRES_PASSWORD="supersecret123456"

POSTGRES_HOST="pg"

RABBIT_MQ_HOST = "rabbitmq"

POSTGRES_PORT="5432"

POSTGRES_USER="admin"

EMAIL_HOST_USER="Ваша почта"

EMAIL_HOST_PASSWORD="Ваш пароль"
```
## DRF API
API доступно по адресу /api/v1/,  
так же доступен swagger на страницах /swagger/ и /redoc/

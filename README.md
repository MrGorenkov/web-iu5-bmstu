# Expertises Artwork — Backend

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat-square&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4-092E20?style=flat-square&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-REST-A30000?style=flat-square)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-336791?style=flat-square&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![MinIO](https://img.shields.io/badge/MinIO-S3-C72E49?style=flat-square&logo=minio&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)

Серверная часть сервиса экспертизы произведений искусства. Курсовая по дисциплине «Разработка интернет-приложений» (МГТУ им. Н. Э. Баумана, ИУ-5, 5 семестр).

> Парный фронтенд: [artwork-frontend](https://github.com/MrGorenkov/artwork-frontend).

## Что реализовано

- REST API на Django REST Framework для каталога картин и заявок на экспертизу
- Авторизация по сессионным ключам, хранение сессий в Redis
- Загрузка и хранение изображений в объектном хранилище MinIO (S3-совместимое API через `minio` + `boto3`)
- Кластер из 4 нод MinIO с реплицированием в Docker Compose
- Генерация QR-кодов для заявок (`qrcode`/`Pillow`)
- Документация API в Swagger UI через `drf-yasg`
- Раздельные роли пользователей: клиент и эксперт-менеджер
- Кастомные классы аутентификации `AuthBySessionID`, `IsAuth`, `IsManagerAuth`

## Архитектура

```
                  ┌────────────────┐
                  │  Frontend (JS) │
                  └────────┬───────┘
                           │ REST
                  ┌────────▼───────┐       ┌──────────────┐
                  │   Django API   │ ◄─────│   Nginx      │
                  │  (DRF)         │       └──────────────┘
                  └───┬────────┬───┘
            sessions  │        │  files
                  ┌───▼──┐  ┌──▼─────────────┐
                  │Redis │  │ MinIO (4 ноды) │
                  └──────┘  └────────────────┘
                            ┌────────────────┐
                            │  PostgreSQL    │
                            └────────────────┘
```

## Стек

- **Backend** — Django 4, Django REST Framework
- **Хранилище** — PostgreSQL (основная БД), Redis (сессии), MinIO (изображения)
- **Документация** — drf-yasg (Swagger), ReDoc
- **Развёртывание** — Docker Compose, Nginx (reverse proxy), 4-нодовый MinIO-кластер
- **Прочее** — boto3, qrcode, Pillow, argon2 для хеширования паролей

## Структура

```
backend/
├── artwork/
│   ├── models.py          # Painting, Expertise, ExpertiseItem
│   ├── views.py           # эндпоинты заявок и картин
│   ├── serializers.py     # DRF-сериализаторы
│   ├── auth.py            # классы аутентификации
│   ├── minio.py           # загрузка/удаление файлов в MinIO
│   ├── redis.py           # session storage
│   └── services/
│       └── qr_generate.py # генерация QR-кодов заявок
├── server_config/         # settings, urls, wsgi
└── manage.py
```

## API

Документация генерируется автоматически в Swagger UI (через `drf-yasg`):

- `GET /swagger/` — интерактивная документация
- `GET /api/paintings/` — каталог картин
- `POST /api/expertises/` — создание заявки на экспертизу
- `GET /api/expertises/{id}/` — детали заявки
- `POST /api/auth/login/` — вход (создаёт сессию в Redis)

## Запуск

```bash
# поднять кластер из 4 MinIO, PostgreSQL, Redis, бэкенд и nginx
docker compose up -d --build

# выполнить миграции
docker compose exec backend python manage.py migrate

# создать суперпользователя
docker compose exec backend python manage.py createsuperuser
```

После запуска:
- API: `http://localhost/api/`
- Swagger: `http://localhost/swagger/`
- MinIO Console: `http://localhost:9001/`

## Ссылки

- [artwork-frontend](https://github.com/MrGorenkov/artwork-frontend) — клиентская часть приложения

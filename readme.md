# Kitten Management API

Kitten Management API — это приложение, позволяющее управлять котятами, породами котят, а также оценивать котят. API реализован на основе Django и Django REST Framework, с поддержкой аутентификации через JWT и подробной Swagger-документацией, используя `drf-yasg`.

## Стек технологий

- **Django** — Основной фреймворк для создания веб-приложений.
- **Django REST Framework (DRF)** — Инструмент для создания API на базе Django.
- **PostgreSQL** — База данных.
- **JWT (JSON Web Tokens)** — Для аутентификации пользователей.
- **drf-yasg** — Инструмент для автоматической генерации Swagger-документации.
- **Docker** — Для контейнеризации приложения.
- **Django Filters** — Для фильтрации запросов API.

## Запуск с использованием Docker

```bash 
cd kitten_expo
```
```bash 
docker compose -f docker-compose.yml up -d --build
```

## Ссылка на API
### http://localhost:8000/swagger

## Данные для получения токена
### Получите токен в ручке /token/ с данными:
{
  "username": "user1",
  "password": "user1"
}
или 
{
  "username": "user2",
  "password": "user2"
}

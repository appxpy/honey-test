# HoneyTest: REST API для управления задачами

REST API для управления списком задач (ToDo list) с аутентификацией, комментариями, файлами и расширенной документацией.

## Технологии

- **Python 3.11**
- **Django 5.1**
- **Django REST Framework**
- **PostgreSQL**
- **Docker** + **Docker Compose**
- **JWT-аутентификация**
- **drf-spectacular** (документация OpenAPI)

## Задачи со звездочкой

- ✅ Полный CRUD для задач
- 🔐 JWT-аутентификация
- 💬 Комментарии к задачам
- 📁 Прикрепление файлов к задачам
- 🔍 Фильтрация, поиск и сортировка:
  - Фильтр по статусу
  - Поиск по названию/описанию
  - Сортировка по дате создания и статусу
- 📚 Автоматическая документация API
- 🧪 Покрытие тестами

## Запуск проекта

### Требования
- Установленные Docker и Docker Compose

1. Клонировать репозиторий:
```bash
git clone git@github.com:appxpy/honey-test.git
cd honeyTest
```

2. Запустить сервисы
```bash
docker-compose up --build
```

Сервисы будут доступны:

- API: http://localhost:8000/api/
- Документация (Swagger): http://localhost:8000/api/docs/
- PGAdmin: http://localhost:5050/

API Endpoints

| Метод  | Эндпоинт                      | Описание                      |
|--------|-------------------------------|-------------------------------|
| POST   | /api/token/                   | Получить JWT-токен            |
| POST   | /api/token/refresh/           | Обновить JWT-токен            |
| POST   | /api/token/verify/            | Проверить JWT-токен           |
| GET    | /api/tasks/                   | Список задач                  |
| POST   | /api/tasks/                   | Создать задачу                |
| GET    | /api/tasks/{id}/              | Получить задачу               |
| PUT    | /api/tasks/{id}/              | Обновить задачу               |
| PATCH  | /api/tasks/{id}/              | Частично обновить задачу      |
| DELETE | /api/tasks/{id}/              | Удалить задачу                |
| GET    | /api/tasks/{id}/comments/     | Список комментариев           |
| POST   | /api/tasks/{id}/comments/     | Добавить комментарий          |
| GET    | /api/tasks/{id}/comments/{id} | Получить комментарий          |
| PUT    | /api/tasks/{id}/comments/{id} | Обновить комментарий          |
| PATCH  | /api/tasks/{id}/comments/{id} | Частично обновить комментарий |
| DELETE | /api/tasks/{id}/comments/{id} | Удалить комментарий           |

## Тестирование

Для запуска всех тестов выполнить команду:
```bash
docker-compose run web python manage.py test todo.tests
```

## Конфигурация

Настройки БД и приложения задаются через переменные окружения в `docker-compose.yaml`:

```yaml
environment:
  DB_ENGINE: django.db.backends.postgresql
  DB_NAME: honey_db
  DB_USER: honey_user
  DB_PASSWORD: honey_password
  DB_HOST: db
  DB_PORT: 5432
```

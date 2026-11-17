# Blog API

REST API для ведения блога. Проект разработан на Django REST Framework с использованием PostgreSQL и JWT-аутентификации.

## 1. Технологии

- Python 3
- Django
- Django REST Framework
- PostgreSQL
- Docker и Docker Compose
- Simple JWT
- drf-spectacular (Swagger / OpenAPI)

## 2. Функциональность

- Регистрация пользователей.
- JWT-аутентификация.
- Создание, просмотр, редактирование и удаление постов.
- Просмотр опубликованных постов для гостей.
- Создание постов авторизованными пользователями.
- Управление постами только их авторами.
- Добавление комментариев к постам.
- Просмотр одобренных комментариев.
- Редактирование и удаление комментариев их авторами.
- Пагинация списка постов.
- Автоматическая API-документация.

## 3. Структура проекта

```text
blog_api/
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── blog/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── permissions.py
│   ├── urls.py
│   └── ...
│
├── docker-compose.yml
├── manage.py
├── requirements.txt
└── README.md
```

## 4. Установка и запуск

### Клонирование репозитория

```bash
git clone YOUR_REPOSITORY_URL
cd blog_api
```

### Создание виртуального окружения

```bash
python3 -m venv venv
```

Активация:

Linux / macOS:

```bash
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Настройка PostgreSQL через Docker

Запуск контейнера:

```bash
docker compose up -d
```

Проверка контейнеров:

```bash
docker compose ps
```

### Настройка переменных окружения

Создайте файл `.env` в корне проекта и укажите настройки базы данных и Django.

Пример:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=blog
DB_USER=blog
DB_PASSWORD=blog
DB_HOST=localhost
DB_PORT=5432
```

Названия переменных должны соответствовать настройкам подключения в `config/settings.py`.

### Применение миграций

```bash
python manage.py makemigrations
python manage.py migrate
```

### Создание администратора

```bash
python manage.py createsuperuser
```

### Запуск сервера

```bash
python manage.py runserver
```

Проект будет доступен:

```text
http://127.0.0.1:8000/
```

## 5. API Endpoints

Базовый адрес:

```text
/api/v1/
```

### Аутентификация

| Метод | Endpoint | Описание |
|---|---|---|
| POST | `/api/v1/auth/register/` | Регистрация |
| POST | `/api/v1/auth/token/` | Получение JWT-токенов |
| POST | `/api/v1/auth/token/refresh/` | Обновление access-токена |

### Посты

| Метод | Endpoint | Описание |
|---|---|---|
| GET | `/api/v1/posts/` | Список опубликованных постов |
| POST | `/api/v1/posts/` | Создание поста |
| GET | `/api/v1/posts/{id}/` | Подробная информация о посте |
| PUT | `/api/v1/posts/{id}/` | Редактирование поста |
| PATCH | `/api/v1/posts/{id}/` | Частичное изменение поста |
| DELETE | `/api/v1/posts/{id}/` | Удаление поста |

### Комментарии

| Метод | Endpoint | Описание |
|---|---|---|
| GET | `/api/v1/posts/{id}/comments/` | Список комментариев поста |
| POST | `/api/v1/posts/{id}/comments/` | Добавление комментария |
| PUT | `/api/v1/comments/{id}/` | Редактирование комментария |
| PATCH | `/api/v1/comments/{id}/` | Частичное изменение комментария |
| DELETE | `/api/v1/comments/{id}/` | Удаление комментария |

## 6. JWT-аутентификация

Для регистрации отправьте POST-запрос:

```json
{
    "username": "testuser",
    "password": "StrongPassword123!"
}
```

Для получения токенов:

```json
{
    "username": "testuser",
    "password": "StrongPassword123!"
}
```

В заголовок запросов, требующих авторизации, добавьте:

```text
Authorization: Bearer YOUR_ACCESS_TOKEN
```

## 7. Права доступа

- Неавторизованные пользователи могут просматривать опубликованные посты.
- Авторизованные пользователи могут создавать посты.
- Только автор поста может изменять и удалять его.
- Авторизованные пользователи могут добавлять комментарии.
- Только автор комментария может изменять и удалять его.
- Пользователи не могут самостоятельно подтверждать свои комментарии.
- Неодобренные комментарии не отображаются в публичном API.

## 8. Пагинация

Для получения списка постов используется пагинация.

Пример запроса:

```text
GET /api/v1/posts/?page=1&page_size=10
```

Пример ответа:

```json
{
    "total": 25,
    "next": "http://127.0.0.1:8000/api/v1/posts/?page=2",
    "previous": null,
    "results": []
}
```

## 9. API-документация

Документация генерируется автоматически с помощью drf-spectacular.

Swagger UI:

```text
http://127.0.0.1:8000/api/docs/
```

ReDoc:

```text
http://127.0.0.1:8000/api/redoc/
```

OpenAPI Schema:

```text
http://127.0.0.1:8000/api/schema/
```

## 10. Автор проекта

Разработано в рамках учебного проекта по созданию REST API на Django REST Framework.
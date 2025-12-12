TODO API + WebSocket + Фоновая задача

## Цель работы

Разработать полноценный серверный backend на FastAPI, реализующий:

### Функциональность
* **REST API** для управления списком задач (TODO-list)
  - `GET /tasks` — список всех задач
  - `GET /tasks/{id}` — получить одну задачу
  - `POST /tasks` — создать новую задачу
  - `PATCH /tasks/{id}` — частичное обновление задачи
  - `DELETE /tasks/{id}` — удалить задачу
  - `POST /task-generator/run` — принудительно вызвать фоновую задачу

* **WebSocket-канал** для уведомлений клиентов в реальном времени
  - `GET /ws/tasks` — подключение к потоку событий задач
  - События: `task_created`, `task_updated`, `task_deleted`

* **Фоновую задачу**, которая периодически наполняет базу данных
  - Загрузка данных со сторонних источников через `httpx`
  - Асинхронное добавление задач в БД

* **Асинхронная работа с базой данных** — SQLAlchemy + asyncpg

### Стек технологий
- **Backend**: FastAPI 0.123+, Uvicorn
- **Database**: PostgreSQL 16, SQLAlchemy 2.0+ (async)
- **ORM Migrations**: Alembic
- **WebSocket**: Starlette WebSocket
- **HTTP Client**: httpx
- **Config**: Pydantic Settings
- **Containerization**: Docker, Docker Compose

---

## Быстрый старт (Docker Compose)

### Требования
- Docker и Docker Compose

### Установка и запуск

1. **Склонировать репозиторий:**
   ```bash
   git clone https://github.com/KomotsKE/FastAPITodoBackend.git
   cd FastAPITodoBackend
   ```

2. **Создать файл `.env` из примера:**
   ```bash
   cp .env.example .env
   ```
   По умолчанию содержимое:
   ```
    PG_HOST=pg_db
    PG_USER=postgres
    PG_PASSWORD=postgres
    PG_DB=todo_list_db
    PG_PORT=5432
   ```

3. **Запустить приложение с помощью Docker Compose:**
   ```bash
   docker-compose up -d
   ```

## Структура проекта

```
FastAPITodoBackend/
├── src/
│   ├── api/
│   │   ├── main.py                 # FastAPI приложение с подключением роутеров
│   │   └── endpoints/
│   │       ├── tasks_endpoints.py  # REST API эндпоинты для задач
│   │       ├── ws_endpoints.py     # WebSocket эндпоинт
│   │       └── background_task_endpoints.py
│   ├── database/
│   │   ├── models/
│   │   │   ├── base.py             # Declarative base для SQLAlchemy
│   │   │   └── task.py             # Модель Task (UUID, title, description, completed, created_at)
│   │   ├── session.py              # Async engine и sessionmaker
│   │   └── migrations/             # Alembic миграции
│   │       ├── env.py
│   │       ├── alembic.ini
│   │       └── versions/
│   ├── schemas/
│   │   ├── task.py                 # Pydantic схемы: TaskCreate, TaskUpdate, TaskOut
│   │   └── ws_events.py            # WebSocket события: TaskEventType enum, TaskEvent
│   ├── websocket/
│   │   └── connection_manager.py   # ConnectionManager для управления WS соединениями
│   └── config.py                   # Pydantic Settings конфигурация
├── Dockerfile                       # Docker образ приложения
├── docker-compose.yml              # Docker Compose конфиг (app + PostgreSQL)
├── alembic.ini                     # Alembic конфигурация
├── requirements.txt                # Python зависимости
├── .env.example                    # Пример переменных окружения
└── README.md                       # Этот файл
```

Swagger
<img width="1919" height="668" alt="image" src="https://github.com/user-attachments/assets/cc95ec7a-5bb5-4a48-861b-e6d3419089d8" />

Websocket
<img width="1118" height="208" alt="image" src="https://github.com/user-attachments/assets/874477ad-c863-4336-831c-b4190f1bfaad" /


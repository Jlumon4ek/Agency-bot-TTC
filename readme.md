# Тестовое задание TTC

## Описание проекта

Проект представляет собой приложение, использующее следующие технологии:

- **SQLAlchemy** для работы с базой данных.
- **Aiogram** для реализации телеграм-бота.
- **OpenAI API** для работы с искусственным интеллектом.
- **PostgreSQL** в качестве базы данных.
- **Alembic** для управления миграциями.
- **Redis** для кеширования и хранения данных.

## Структура проекта

```
.
├── app
│   ├── alembic.ini                # Конфигурация Alembic
│   ├── dockerfiles
│   │   └── backend.dockerfile     # Dockerfile для backend
│   ├── example.env                # Пример файла переменных окружения
│   ├── migration
│   │   ├── env.py                 # Файл конфигурации Alembic
│   │   ├── script.py.mako         # Шаблон для миграций
│   │   └── versions               # Каталог с миграциями
│   │       ├── 707b4ed283a4_initial_database.py
│   │       ├── dd0ed82fbeec_create_user_table.py
│   ├── requirements
│   │   └── requirements.txt       # Зависимости Python
│   └── src
│       ├── agents                 # Логика для генерации и оценки данных
│       │   ├── evaluator.py
│       │   ├── generator.py
│       │   └── supervisor.py
│       ├── config.py              # Конфигурация проекта
│       ├── constants.py           # Константы проекта
│       ├── dao                    # Работа с базой данных
│       │   ├── base.py
│       │   ├── dao.py
│       │   ├── database.py
│       ├── main.py                # Точка входа
│       └── users                  # Логика для управления пользователями
│           ├── models.py
│           ├── router.py
│           ├── service.py
│           ├── states.py
│           └── validator.py
├── data                           # Данные проекта
├── docker-compose.yml             # Конфигурация Docker Compose
├── Makefile                       # Автоматизация команд
└── readme.md                      # Документация проекта
```

## Установка и запуск

1. **Склонируйте репозиторий:**

   ```bash
   git clone https://github.com/your-repo.git
   cd Тестовое-задание-TTC
   ```

2. **Скопируйте файл переменных окружения:**

   ```bash
   cp app/example.env .env
   ```

3. **Запустите контейнеры Docker:**

   ```bash
   make up
   ```

4. **Примените миграции:**

   ```bash
   make migrate
   ```

5. **Войдите в контейнер для выполнения дополнительных команд:**

   ```bash
   make bash
   ```

## Зависимости

Все зависимости описаны в файле `app/requirements/requirements.txt`. Убедитесь, что они установлены перед локальным запуском проекта.

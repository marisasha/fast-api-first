# KINOLOG 

Веб приложение для просмотра данных из операций OLAP куба для таблицы студентов , курсов и успеваемости.

# Tech Stack

- Python
- FastApi
- PostgreSQL
- Jinja2 Templates

# Очередность действий для запуска проекта
1. Создать файл `.env` с настройками для PostgreSQL

```.env
DB_USERNAME= postgres
DB_PASSWORD= postgres // можно любой другой
DB_HOST= localhost 
DB_PORT= 5432
DB_NAME= university // можно любое другое
```

2. Создать виртуальное окружение и скачать библиотеки из папки requirments

Для Windows
```cmd
python -m venv venv
call venv/scripts/activate
pip install -r requirements/requirements_windows.txt
```
Для MacOs и Linux
```cmd
python3 -m venv venv
source venv/bin/activate
pip install -r requirements/requirements_linux.txt
```

3. Создание миграции таблиц

Создадим файл alembic.ini

```alembic.ini
[alembic]
script_location = %(here)s/alembic
prepend_sys_path = .
path_separator = os
sqlalchemy.url = postgresql://postgres:{ваш пароль от БД}@{используемый хост}:{используемый порт}/{название бд}
[post_write_hooks]
[loggers]
keys = root,sqlalchemy,alembic
[handlers]
keys = console
[formatters]
keys = generic
[logger_root]
level = WARNING
handlers = console
qualname =
[logger_sqlalchemy]
level = WARNING
handlers =
qualname = sqlalchemy.engine
[logger_alembic]
level = INFO
handlers =
qualname = alembic
[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic
[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

Применим миграции
```cmd
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```


4. Запустить приложение
```cmd
uvicorn src.main:app --reload  
```

# Project Structure

- **alembic** — инструмент для миграции
- **requirements** — папка с зависимостями проекта
- **templates** — шаблоны страниц
- **src** — папка с исходным кодом проекта
  - **src/university** - папка с бизнес логикой 
  - **src/database** - настроки postgresql
  - **src/main** - точка запуска проекта
  - **src/router** - гланый маршрутизатор


# api_yamdb

### Описание проетка:

API для проекта YAMDB

### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Viktor-Gostyaikin/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### Примеры запросов к api:

GET-Response: http://127.0.0.1:8000/api/v1/titles/1/reviews/
Request:


[
    {
        "id": 1,
        "author": "author",
        "image": "",
        "text": "text",
        "pub_date": "pub_date",
        "group": null
    },
]


POST-Response: http://127.0.0.1:8000/api/v1/posts/
Поле text обязательное:

{
    "text": "text"
}

Request:

{
    "id": 5,
    "author": "admin",
    "image": "",
    "text": "text",
    "pub_date": "pub_date",
    "group": null
}


GET-Response: http://127.0.0.1:8000/api/v1/posts/1/comments/
Request:

[
    {
        "id": 1,
        "author": "author",
        "text": "text",
        "created": "created",
        "post": 1
    },
]


POST-Response: http://127.0.0.1:8000/api/v1/follow/
Поле following обязательное:

{
    "following": "test"
}

Request:

{
    "id": 4,
    "user": "user",
    "following": "test"
}

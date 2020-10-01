## Original task:
- https://github.com/avito-tech/auto-backend-trainee-assignment
- Задача:
- Нужно сделать HTTP сервис для сокращения URL наподобие [Bitly](https://bitly.com/) и других сервисов.
- UI не нужен, достаточно сделать JSON API сервис.
- Должна быть возможность:
    - 🟩 да 🔹 сохранить короткое представление заданного URL
    - 🟩 да 🔹 перейти по сохраненному ранее короткому представлению и получить redirect на соответствующий исходный URL
- Требования:
    - 🟩 Python 🔹 Язык программирования: Go/Python/PHP/Java/JavaScript
    - 🟨 README 🔹 Предоставить инструкцию по запуску приложения. В идеале (но не обязательно) – использовать контейнеризацию с возможностью запустить проект командой [`docker-compose up`](https://docs.docker.com/compose/)
    - 🟩 PostgreSQL & Redis 🔹 Требований к используемым технологиям нет - можно использовать любую БД для персистентности
    - 🟩 да 🔹 Код нужно выложить на github (просьба не делать форк этого репозитория, чтобы не плодить плагиат)
- Усложнения:
    - 🟥 нет 🔹 Написаны тесты (постарайтесь достичь покрытия в 70% и больше)
    - 🟩 да 🔹 Добавлена валидация URL с проверкой корректности ссылки
    - 🟩 да 🔹 Добавлена возможность задавать кастомные ссылки, чтобы пользователь мог сделать их человекочитаемыми - [http://bit.ly/avito-auto-be](http://bit.ly/avito-auto-be)
    - 🟥 нет (использовал Redis as cache) 🔹 Проведено нагрузочное тестирование с целью понять, какую нагрузку на чтение может выдержать наш сервис
    - 🟩 да (digitalocean.com - https://s.42q.ru) 🔹 Если вдруг будет желание, можно слепить простой UI и выложить сервис на бесплатный хостинг - Google Cloud, AWS и подобные. 

## Requirements:

* Python 3.6+
* PostgreSQL 9.6+
* Redis 2.0+
* FastAPI & Uvicorn

## How-to

* Update python  
https://tech.serhatteker.com/post/2019-12/how-to-install-python38-on-ubuntu/

* Install PostgreSQL  
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04

* Install Redis  
https://www.digitalocean.com/community/tutorials/how-to-install-and-secure-redis-on-ubuntu-18-04

* Isntall FastAPI & Uvicorn  
https://fastapi.tiangolo.com/#installation


## Local run

* `pip install pydantic[dotenv] sqlalchemy databases asyncpg alembic aioredis`
* `pip install python3-psycopg2 libpq-dev psycopg2`
* `cp .env_example .env`
* Setup .env file. `./init_script.sh` can help to create a database in PostgreSQL and add configs to .env
* `alembic upgrade head`
* `uvicorn app.main:app --reload --port 8000`

## How to use

For example a 🔸target_url🔸 is https://www.youtube.com/watch?v=dQw4w9WgXcQ

* To create short link do GET request with your browser or curl like this http://127.0.0.1:8000/set/🔸target_url🔸  
    * Ex.: http://127.0.0.1:8000/set/https://www.youtube.com/watch?v=dQw4w9WgXcQ  
    * As response you will get something like this: 
    ```json
    {
      "ok":true,
      "msg":"ok",
      "request_url":"http://127.0.0.1:8000/set/https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "target_url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "redirect_url":"http://127.0.0.1:8000/DKJL"
    }
    ```
 
 * For get information about short link with 🔸code🔸 do GET request like this http://127.0.0.1:8000/get/🔸code🔸
    * Ex.: http://127.0.0.1:8000/get/DKJL
    * As response you will get something like this: 
    ```json
    {
       "ok":true,
       "link":"https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    }
    ```
   
  * For redirect with 🔸code🔸 do GET request like this http://127.0.0.1:8000/🔸code🔸
    * Ex.: http://127.0.0.1:8000/DKJL
    
  * To create short link with given 🔹code🔹 do GET request with your browser or curl like this http://127.0.0.1:8000/set_with/🔹code🔹/🔸target_url🔸  
    * Ex.: http://127.0.0.1:8000/set_with/Rick/https://www.youtube.com/watch?v=dQw4w9WgXcQ  
    * As response you will get something like this: 
    ```json
    {
      "ok":true,
      "msg":"ok",
      "request_url":"http://127.0.0.1:8000/set_with/Rick/https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "target_url":"https://www.youtube.com/watch?v=dQw4w9WgXcQ",
      "redirect_url":"http://127.0.0.1:8000/Rick"
    }
    ```
   
  * For turn off redirect for 🔸code🔸 do GET request like this http://127.0.0.1:8000/turn_off/🔸code🔸
    * Ex.: http://127.0.0.1:8000/turn_off/DKJL
    
  * For turn on redirect for 🔸code🔸 do GET request like this http://127.0.0.1:8000/turn_on/🔸code🔸
    * Ex.: http://127.0.0.1:8000/turn_on/DKJL
    
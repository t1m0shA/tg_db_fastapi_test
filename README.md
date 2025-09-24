# Как запустить
### 1. Cклонировать этот репозиторий
```sh
git clone https://github.com/t1m0shA/tg_db_fastapi_test.git
```
##
### 2. Перейти в рабочую папку
```sh
cd tg_db_fastapi_test
```
##
### 3. Создать + активировать локальное окружение (для Telethon проекта)
```sh
python -m venv venv
```
```sh
source venv/bin/activate
```
##
### 4. Установить зависимости локально
```sh
pip install -r requirements.txt
```
##
### 5. Вставить данные в .env
Переменные TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE, TELEGRAM_CHAT
##
### 6. Запустить FastAPI + PostgreSQL в Docker
```sh
docker compose up --build -d
```
##
### 7. Посмотреть эндпоинты на [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
Чтобы проверить БД нужно сначала сделать POST к ```/create_tables_raw``` а потом к ```/seed_database```. После этого 
можно получить результат запроса, который вернёт последнее сообщение каждого пользователя по GET ```/last_messages```.
##
### 8. Запустить и проверить Telethon проект
```sh
python -m tel.main
```
Он также еще делает запрос к FastAPI на проверку lead/not_lead
##


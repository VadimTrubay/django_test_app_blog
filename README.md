# django_test_app_blog

# How to start for developers:
- update project from Git https://github.com/VadimTrubay/django_test_app_blog
- create environment
- activate environment
- rename files `.env_example` file to `.env` and fill in your credentials
- pip install -r requirements.txt
- run docker application

- run in terminal: `docker-compose build` -> build Web + Postgres + Bot
- run in terminal: `docker-compose up` -> up Web + Postgres + Bot
- run in terminal: `python manage.py migrate` -> migrate current models to DB
- run in terminal: `python manage.py createsuperuser` -> create super user admin
- run in terminal: `python manage.py runserver` -> starts Django server
- run in terminal: `python bot.py` -> starts telegram bot
- you need create telegram bot in Telegram and fill in your credentials token to `.env`
- for start scraping_app run in terminal `python parse_and_save_news.py`
- 

- now you have access to:
- http://127.0.0.1:8000/api/docs -> Swagger documentation DRF Application


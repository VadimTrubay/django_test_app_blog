# django_test_app_blog

# How to start for developers:
- update project from Git https://github.com/VadimTrubay/django_test_app_blog
- create environment 
- pip install -r requirements.txt
- create in root folder your own .env file like .env.example
- run docker application

- run in terminal: `docker-compose up` -> up Redis + Postgres
- run in terminal: `alembic upgrade head` -> implementation current models to DB
- run in terminal: `uvicorn main:app --host localhost --port 8000 --reload` -> start application
- run in terminal: `streamlit run main_app.py` -> start front application

- now you have access to:
- http://127.0.0.1:8000/docs -> Swagger documentation
- http://localhost:8501/ -> Streamlit frontend

# Shut off
- terminal with uvicorn -> Press CTRL+C to quit
- terminal with docker run: `docker-compose down` -> shut Redis+Postgres

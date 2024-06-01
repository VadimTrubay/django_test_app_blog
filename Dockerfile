FROM python:3.11

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

# Запустимо нашу програму всередині контейнера
CMD ["python", "test_app_blog/manage.py", "runserver", "0.0.0.0:8000"]

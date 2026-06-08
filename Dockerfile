FROM python:3.12-slim

RUN mkdir -p /usr/src/app

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN pip install -r ./requirements.txt

EXPOSE 5000

ENTRYPOINT [ "gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "app:app" ]
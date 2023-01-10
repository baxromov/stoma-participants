FROM python:3

RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y locales
RUN apt-get install -y build-essential libpq-dev
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/


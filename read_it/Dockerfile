FROM python:3.10-slim

WORKDIR /read_it

COPY ./requirements.txt /read_it/requirements.txt
COPY ./read_it /read_it/read_it
COPY ./db_logging /read_it/db_logging
COPY ./goodreads_scraping /read_it/goodreads_scraping
COPY ./manage.py /read_it/manage.py

RUN apt-get update
RUN apt-get install -y libpq-dev gcc
RUN pip install --upgrade pip
RUN pip install -r /read_it/requirements.txt

CMD python3 -m gunicorn --bind :80 read_it.wsgi:application

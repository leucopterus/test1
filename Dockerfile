FROM python:3.8
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
RUN chmod 755 /code/wait_for_psql_avail.sh \
    && chmod 755 /code/wait_for_web_avail_celery.sh \
    && chmod 755 /code/wait_for_web_avail_celery_beat.sh

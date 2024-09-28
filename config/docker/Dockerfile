FROM python:3.11-slim

RUN apt-get update && apt-get install -y supervisor && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN pip install --no-cache-dir --upgrade pip==24.2

COPY config/docker/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

RUN python manage.py collectstatic --noinput

COPY config/docker/supervisord-web.conf /etc/supervisor/conf.d/
#COPY config/docker/supervisord-celery.conf /etc/supervisor/conf.d/

COPY config/script/start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000

CMD ["/start.sh"]

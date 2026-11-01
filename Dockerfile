FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . ./
RUN mkdir -p media/uploads staticfiles \
    && python manage.py collectstatic --noinput

ENV PORT=3000
ENV DJANGO_DEBUG=False
ENV DJANGO_ALLOWED_HOSTS=*
EXPOSE 3000

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:${PORT:-3000} --workers 2 --threads 2 --timeout 60"]

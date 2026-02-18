FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . /app/

# Collect static files for Whitenoise
RUN SECRET_KEY=building_static_assets python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "lab_one_url_shortener.wsgi:application", "--bind", "0.0.0.0:8000"]

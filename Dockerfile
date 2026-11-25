# Sticky Notes - Django application image
FROM python:3.13-slim

# Do not write .pyc files and send log output straight to the terminal.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install the dependencies first so this layer is cached between builds.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project (the folder that contains manage.py).
COPY sticky_notes/ .

# Default configuration for running the container locally or in a
# Docker playground. Override these with "docker run -e ..." or
# "--env-file .env"; always set your own DJANGO_SECRET_KEY outside of
# local testing.
ENV DJANGO_DEBUG=True \
    DJANGO_ALLOWED_HOSTS=*

EXPOSE 8000

# Apply database migrations, then start the web server on all interfaces
# so that it is reachable from outside the container.
CMD ["sh", "-c", "python manage.py migrate --noinput && python manage.py runserver 0.0.0.0:8000"]

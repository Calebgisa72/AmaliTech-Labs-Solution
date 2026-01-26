# URL Shortener Microservice (Django & DRF)

## Overview

A URL shortener microservice built with Django and Django REST Framework. This project uses Redis for data storage and caching, running in a Dockerized environment. It demonstrates clean architecture, REST API development, and documented with Swagger/OpenAPI.

## Architecture

The application runs as two Docker services:

1.  **Web**: Django application running with Gunicorn.
2.  **Redis**: Primary data store for URL mappings and analytics.

**Data Flow:**

- URL creation and retrieval bypass the Django ORM and interact directly with Redis via a Service layer.
- User clicks are tracked in Redis Lists and Sorted Sets for analytics.

## Folder Structure

```
.
├── Dockerfile              # Docker image definition
├── docker-compose.yml      # Service orchestration
├── requirements.txt        # Python dependencies
├── manage.py               # Django management script
├── .env.example            # Environment configuration template
├── lab_one_url_shortener/  # Project configuration
│   ├── settings.py         # Config including Redis & drf-spectacular
│   └── urls.py             # Main routing & Swagger setup
└── url_shortener/          # Application Logic
    ├── services.py         # Business logic & Redis interactions
    ├── redis_client.py     # Redis connection wrapper
    ├── views.py            # API ViewControllers
    └── serializers.py      # Data validation & serialization
```

## Setup & Running

1.  **Clone the repository**.
2.  **Environment Setup**:
    Copy `.env.example` to `.env`:

    ```bash
    cp .env.example .env
    ```

    (Default settings in `.env.example` work out-of-the-box with Docker Compose).

3.  **Run with Docker Compose**:
    ```bash
    docker-compose up --build
    ```
    This will start the Django app on port `8000` and Redis on port `6379`.

## API Documentation

Interactive API documentation (Swagger UI) is available at:
**[http://localhost:8000/swagger/](http://localhost:8000/swagger/)**

### Endpoints

- `POST /api/shorten/` - Shorten a URL.
- `GET /go/<short_code>/` - Redirect to original URL.
- `GET /api/top-clicked/` - Get top 4 most clicked URLs.
- `GET /api/user-clicks/` - Get click history for the current user IP.

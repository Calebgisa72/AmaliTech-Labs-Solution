# URL Shortener Backend (Django & DRF)

## Overview

This is the primary backend application for the URL shortener microservices ecosystem, built with Django and Django REST Framework. It handles core URL shortening, user authentication, link analytics, and integrates with Celery for asynchronous background processing. It stores relational data in PostgreSQL and uses Redis for high-speed caching and functioning as a Celery message broker.

## Architecture & Integration

This service operates as the main entry point (running on port `8000`) and orchestrates tasks with other components:

1.  **Web**: Django application running with Gunicorn or Django dev server.
2.  **PostgreSQL**: Primary relational data store for Users, URLs, and Analytics data.
3.  **Redis**: Broker for Celery tasks and high-performance caching for frequently accessed URL redirects and analytics.
4.  **Celery & Celery Beat**: Asynchronous task workers to process clicks data, scrape external metadata, and handle scheduled background jobs without blocking HTTP responses.
5.  **URL Preview Microservice**: Interacts with the `url_preview` service (expected on port `8001`) to securely scrape the target's title, description, and favicon for newly shortened links.

## Folder Structure

```text
.
├── Dockerfile              # Docker image definition for the web/celery workers
├── docker-compose.yml      # Orchestrates web, db, redis, celery, and url_preview
├── requirements.txt        # Python dependencies
├── manage.py               # Django management script
├── .env.example            # Environment configuration template
├── lab_one_url_shortener/  # Django project configuration (settings, router, celery app)
├── api/                    # Centralized API routing layer mapping sub-apps
├── core/                   # Shared essentials: Auth, Custom Token Views, Middleware
└── url_shortener/          # Core Domain Logic:
    ├── models.py           # Database schemas
    ├── repositories.py     # Data access layer for DB operations
    ├── services.py         # Business logic layer
    ├── preview_service.py  # Abstraction to communicate with `url_preview` microservice
    ├── tasks.py            # Celery asynchronous tasks
    ├── redis_client.py     # Redis connection mapping
    ├── views.py            # API ViewControllers
    └── serializers.py      # Data validation & serialization
```

## Setup & Running

1.  **Environment Setup**:
    Copy `.env.example` to `.env`:

    ```bash
    cp .env.example .env
    ```

    (Default settings in `.env.example` are pre-configured to work with the `docker-compose.yml`.)

2.  **Run with Docker Compose**:
    The recommended way to spin up the full network (Main App, Preview App, DB, Redis, Celery Workers):
    ```bash
    docker-compose up --build
    ```
    This will start the Django app on port `8000`, the Preview app on `8001`, Postgres on `5433` (mapped from 5432), and Redis on `6379`.

## API Documentation

Interactive API documentation (Swagger UI) is available at:
**[http://localhost:8000/swagger/](http://localhost:8000/swagger/)**

### Core Endpoints

- `POST /api/v1/auth/register/` - Register a user.
- `POST /api/v1/auth/login/` - Login and receive JWT.
- `POST /api/v1/auth/refresh/` - Refresh JWT access token.
- `POST /api/v1/urls/shorten/` - Shorten a URL.
- `GET /api/v1/urls/` - List your shortened URLs.
- `GET /api/v1/urls/top-clicked/` - Get top globally clicked URLs.
- `GET /api/v1/urls/user-clicks/` - Get click history for authenticated user.
- `GET /api/v1/analytics/<identifier>/` - Get comprehensive analytics.
- `GET /api/v1/<identifier>/` - Redirect to original URL.
- `GET /health/` - Check server health.

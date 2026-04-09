# Uptime Monitor

A REST API service for monitoring website availability built with FastAPI, PostgreSQL, Redis, and Celery.

## Table of Contents
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Future Improvements](#future-improvements)

## Features
- Monitor website availability at configurable intervals
- Automatic retry on failed checks (3 attempts)
- Uptime percentage and response time statistics
- Check history with pagination
- JWT authentication with refresh token rotation
- Automatic cleanup of old checks
- Monitors restart automatically after server restart

## Tech Stack
- **FastAPI** - REST API framework
- **PostgreSQL** - primary database
- **SQLAlchemy** - async ORM
- **Alembic** - database migrations
- **Celery** - background task queue
- **Redis** - message broker and result backend
- **Docker** - containerization

## Architecture
- `api/` - FastAPI routers
- `services/` - business logic
- `repositories/` - database queries
- `tasks/` - Celery background tasks
- `models/` - SQLAlchemy models
- `schemas/` - Pydantic schemas

## Getting Started

### Prerequisites
- Docker
- Docker Compose

### Installation
```bash
git clone https://github.com/Hlib-Oliinyk/uptime-monitor
cd uptime_monitor
cp .env.example .env
docker-compose up --build -d
docker-compose exec api alembic upgrade head
```

## API Endpoints

### Auth
- `POST /auth/register` - register new user
- `POST /auth/login` - login and get tokens
- `POST /auth/refresh` - refresh access token
- `DELETE /auth/logout` - logout

### Monitors
- `GET /monitor/` - get all monitors
- `POST /monitor/` - create monitor
- `GET /monitor/{id}` - get monitor
- `PATCH /monitor/{id}` - update monitor
- `DELETE /monitor/{id}` - delete monitor

### Checks
- `GET /check/{monitor_id}` - get check history
- `GET /check/{monitor_id}/stats` - get uptime statistics

## Running Tests
```bash
pytest -s -v
```

## Future Improvements
- JSON persistence for data export
- Email/Telegram notifications when monitor goes down
- Response time graphs
- Redis caching for statistics
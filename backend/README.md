# ChronoTasks API – Event-Driven Task Orchestration Engine

A production-grade backend system built with Django and Django REST Framework, demonstrating advanced backend engineering concepts including event-driven architecture, asynchronous processing, caching, and optimized database access.

## 🎯 Core Features

- **Event-Driven Architecture**: Every task operation generates events for asynchronous processing
- **Async Processing**: Background task processing with Celery
- **Advanced Caching**: Redis-based caching for optimized performance
- **JWT Authentication**: Secure token-based authentication
- **Role-Based Access Control**: Admin and User roles with proper permissions
- **Optimized Database Queries**: Efficient query patterns to avoid N+1 problems
- **RESTful API Design**: Clean, paginated, filterable endpoints

## 🏗️ Architecture

### Modular App Structure
- `accounts` - User authentication and role management
- `tasks` - Task management logic
- `events` - Event tracking and processing system
- `core` - Shared utilities, settings, and configurations

## 🛠️ Tech Stack

- **Framework**: Django 4.2+
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **Cache/Queue**: Redis
- **Authentication**: JWT (SimpleJWT)
- **Async Processing**: Celery
- **Task Queue**: Redis (Celery broker)

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Redis 7+

## 🚀 Quick Start

### 1. Clone the repository
```bash
git clone <repository-url>
cd chronotasks-api
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
```bash
cp .env.example .env
# Edit .env with your configuration
```

### 5. Set up PostgreSQL database
```bash
# Create database
createdb chronotasks_db

# Or using psql
psql -U postgres
CREATE DATABASE chronotasks_db;
```

### 6. Run migrations
```bash
python manage.py migrate
```

### 7. Create superuser
```bash
python manage.py createsuperuser
```

### 8. Start Redis (in separate terminal)
```bash
redis-server
```

### 9. Start Celery worker (in separate terminal)
```bash
celery -A chronotasks worker -l info
```

### 10. Run development server
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`

## 📚 API Documentation

### Authentication Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - Login (get JWT tokens)
- `POST /api/auth/token/refresh/` - Refresh access token

### Task Endpoints
- `GET /api/tasks/` - List tasks (with pagination, filtering, search)
- `POST /api/tasks/` - Create task
- `GET /api/tasks/{id}/` - Retrieve task
- `PUT /api/tasks/{id}/` - Update task
- `PATCH /api/tasks/{id}/` - Partial update
- `DELETE /api/tasks/{id}/` - Delete task

### Event Endpoints
- `GET /api/events/` - List events (admin only)
- `GET /api/events/{id}/` - Retrieve event details

### Query Parameters
- `?status=TODO` - Filter by status
- `?priority=HIGH` - Filter by priority
- `?assigned_to=1` - Filter by assigned user
- `?search=keyword` - Search in title/description
- `?page=2` - Pagination

## 🔐 Authentication

All endpoints (except registration and login) require JWT authentication.

Include the token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## 🎭 User Roles

- **ADMIN**: Full access to all resources
- **USER**: Access only to their own tasks

## 🏃 Running Tests

```bash
python manage.py test
```

## 📊 Event-Driven System

Every task operation generates events:
- `TASK_CREATED` - When a task is created
- `TASK_UPDATED` - When a task is modified
- `TASK_COMPLETED` - When a task status changes to DONE
- `TASK_DELETED` - When a task is deleted

Events are processed asynchronously by Celery workers for:
- Logging
- Notifications (simulated)
- Analytics updates

## ⚡ Performance Features

- Redis caching for frequently accessed data
- Query optimization with `select_related` and `prefetch_related`
- API rate limiting
- Database indexing on frequently queried fields

## 📁 Project Structure

```
chronotasks-api/
├── chronotasks/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/             # User management
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── tasks/                # Task management
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── events/               # Event system
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tasks.py          # Celery tasks
│   └── urls.py
├── core/                 # Shared utilities
│   ├── permissions.py
│   ├── pagination.py
│   └── utils.py
├── requirements.txt
├── .env.example
└── manage.py
```

## 🔧 Environment Variables

See `.env.example` for all required environment variables.

## 📝 License

MIT License

## 👨‍💻 Development Phases

This project was built in phases:
- Phase 1: Project setup and structure
- Phase 2: User authentication system
- Phase 3: Task management system
- Phase 4: Event-driven architecture
- Phase 5: Async processing with Celery
- Phase 6: Caching and optimization
- Phase 7: Testing and documentation

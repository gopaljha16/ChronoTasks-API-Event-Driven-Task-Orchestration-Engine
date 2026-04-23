# ChronoTasks - Event-Driven Task Management System

A full-stack task management application with event-driven architecture, built with Django REST Framework (backend) and React (frontend).

## Project Structure

```
chronotasks/
├── backend/          # Django REST API
├── frontend/         # React application
└── README.md         # This file
```

## Features

### Backend (Django REST Framework)
- ✅ JWT Authentication
- ✅ Task CRUD with filtering & search
- ✅ Event-driven architecture
- ✅ Celery async processing
- ✅ Redis caching
- ✅ Rate limiting
- ✅ Comprehensive test suite

### Frontend (React)
- ✅ Modern React 18 UI
- ✅ Tailwind CSS styling
- ✅ Redux Toolkit state management
- ✅ JWT authentication with auto-refresh
- ✅ Complete task management interface
- ✅ Advanced filtering and search
- ✅ Event log (admin only)
- ✅ Responsive design
- ✅ Toast notifications

## Quick Start

### Prerequisites
- Python 3.14+
- Node.js 18+
- Redis Server
- PostgreSQL (optional, SQLite for development)

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
python manage.py migrate
python manage.py create_test_users
python manage.py runserver
```

Backend will run on: http://localhost:8000

### Frontend Setup

```bash
cd frontend
npm install
npm start
```

Frontend will run on: http://localhost:3000

### Redis Setup (for Celery & Caching)

```bash
# Windows (WSL)
sudo service redis-server start

# Docker
docker run -d -p 6379:6379 redis:latest
```

### Celery Worker (Optional)

```bash
cd backend
celery -A chronotasks worker --loglevel=info --pool=solo
```

## API Documentation

API documentation available at:
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- API Docs: See `backend/API_DOCUMENTATION.md`

## Testing

### Backend Tests
```bash
cd backend
python manage.py test
coverage run --source='.' manage.py test
coverage report
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Technology Stack

### Backend
- Django 4.2.7
- Django REST Framework 3.14.0
- PostgreSQL / SQLite
- Redis
- Celery
- JWT Authentication

### Frontend
- React 18.2
- Redux Toolkit 2.2
- Tailwind CSS 3.4
- React Router v6
- Axios with interceptors
- date-fns
- React Toastify

## Project Phases

- ✅ Phase 1: Initial Setup
- ✅ Phase 2: Django Project & Apps
- ✅ Phase 3: User Authentication
- ✅ Phase 4: Task Management
- ✅ Phase 5: Event-Driven Architecture
- ✅ Phase 6: Async Processing (Celery)
- ✅ Phase 7: Caching & Performance
- ✅ Phase 8: Testing & Documentation
- ✅ Phase 9: React Frontend
- 🚧 Phase 10: Production Deployment

## License

MIT License

## Contributors

- Your Name

## Support

For issues and questions, please open an issue on GitHub.

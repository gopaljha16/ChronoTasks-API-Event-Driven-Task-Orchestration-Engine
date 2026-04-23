# Celery Setup Guide

## Prerequisites

1. **Redis** must be installed and running
2. **Python dependencies** must be installed (redis, celery)

## Installing Redis on Windows

### Option 1: Using WSL (Recommended)
```bash
wsl --install
# After WSL is installed:
sudo apt update
sudo apt install redis-server
sudo service redis-server start
```

### Option 2: Using Docker
```bash
docker run -d -p 6379:6379 redis:latest
```

### Option 3: Download Windows Port
Download from: https://github.com/microsoftarchive/redis/releases

## Starting Celery Worker

### Windows (PowerShell)
```powershell
# Activate virtual environment
venv\Scripts\activate

# Start Celery worker
celery -A chronotasks worker --loglevel=info --pool=solo
```

### Linux/Mac
```bash
# Activate virtual environment
source venv/bin/activate

# Start Celery worker
celery -A chronotasks worker --loglevel=info
```

## Testing Celery

### 1. Start Redis
Make sure Redis is running on localhost:6379

### 2. Start Django Server
```bash
python manage.py runserver
```

### 3. Start Celery Worker (in another terminal)
```bash
celery -A chronotasks worker --loglevel=info --pool=solo
```

### 4. Test Celery Tasks
```bash
python manage.py test_celery
```

### 5. Create a Task (triggers async processing)
```bash
# Use the API or Django shell
python manage.py shell

from tasks.models import Task
from django.contrib.auth import get_user_model

User = get_user_model()
user = User.objects.first()

# This will trigger async event processing
task = Task.objects.create(
    title='Test Async Task',
    description='This will trigger Celery',
    created_by=user
)
```

## Monitoring Celery

### Check Task Status
```python
from celery.result import AsyncResult

result = AsyncResult('task-id-here')
print(result.state)
print(result.result)
```

### Celery Flower (Web UI)
```bash
pip install flower
celery -A chronotasks flower
# Visit http://localhost:5555
```

## Common Issues

### Issue: Connection refused to Redis
**Solution**: Make sure Redis is running
```bash
# Check if Redis is running
redis-cli ping
# Should return: PONG
```

### Issue: Tasks not executing
**Solution**: Make sure Celery worker is running
```bash
celery -A chronotasks worker --loglevel=info --pool=solo
```

### Issue: Import errors
**Solution**: Make sure all dependencies are installed
```bash
pip install -r requirements.txt
```

## Production Deployment

For production, use:
- **Supervisor** or **systemd** to manage Celery workers
- **Redis Sentinel** for Redis high availability
- **Celery Beat** for periodic tasks
- **Multiple workers** for better performance

Example systemd service:
```ini
[Unit]
Description=Celery Worker
After=network.target

[Service]
Type=forking
User=www-data
Group=www-data
WorkingDirectory=/path/to/chronotasks
ExecStart=/path/to/venv/bin/celery -A chronotasks worker --loglevel=info

[Install]
WantedBy=multi-user.target
```

# Phase 2: Django Project & Apps Initialization

## Commands to Run (in order):

### 1. Create Virtual Environment
```bash
python -m venv venv
```

### 2. Activate Virtual Environment
```bash
# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Create Django Project
```bash
django-admin startproject chronotasks .
```

### 5. Create Django Apps
```bash
python manage.py startapp accounts
python manage.py startapp tasks
python manage.py startapp events
python manage.py startapp core
```

### 6. Verify Structure
After running the commands, your structure should look like:
```
chronotasks-api/
├── chronotasks/          # Main project folder
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── accounts/             # User management app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── tasks/                # Task management app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── events/               # Event tracking app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── core/                 # Shared utilities app
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## After Setup:

Once you've run all commands, come back and I'll:
1. Configure settings.py
2. Set up database connections
3. Configure installed apps
4. Set up URL routing
5. Create initial configurations

Then you can commit Phase 2!

@echo off
echo Running tests with coverage...
echo.

REM Activate virtual environment
call venv\Scripts\activate

REM Run tests with coverage
coverage run --source='.' manage.py test

REM Generate coverage report
echo.
echo Generating coverage report...
coverage report

REM Generate HTML coverage report
echo.
echo Generating HTML coverage report...
coverage html

echo.
echo Coverage report generated in htmlcov/index.html
echo.
pause

#!/bin/bash

echo "Running tests with coverage..."
echo

# Activate virtual environment
source venv/bin/activate

# Run tests with coverage
coverage run --source='.' manage.py test

# Generate coverage report
echo
echo "Generating coverage report..."
coverage report

# Generate HTML coverage report
echo
echo "Generating HTML coverage report..."
coverage html

echo
echo "Coverage report generated in htmlcov/index.html"

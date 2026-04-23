#!/bin/bash

echo "========================================"
echo "ChronoTasks Frontend Setup"
echo "========================================"
echo ""

echo "Installing dependencies..."
npm install

echo ""
echo "Creating .env file..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created successfully"
else
    echo ".env file already exists"
fi

echo ""
echo "========================================"
echo "Setup Complete!"
echo "========================================"
echo ""
echo "To start the development server, run:"
echo "npm start"
echo ""

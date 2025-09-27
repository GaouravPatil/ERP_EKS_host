#!/bin/bash

# College ERP Quick Start Script
# This script activates the virtual environment and starts the server

echo "🎓 Starting College ERP System..."

# Change to project directory
cd /home/rival/Desktop/python_project

# Check if virtual environment exists
if [ ! -d "rival" ]; then
    echo "❌ Virtual environment 'rival' not found!"
    echo "Please run the setup script first."
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source rival/bin/activate

# Change to Django project directory
cd college_erp_system

# Check if Django is installed
if ! python -c "import django" 2>/dev/null; then
    echo "❌ Django not found! Installing requirements..."
    pip install -r requirements.txt
fi

# Run system check
echo "🔍 Checking system..."
python manage.py check

if [ $? -eq 0 ]; then
    echo "✅ System check passed!"
    echo ""
    echo "🚀 Starting development server..."
    echo "👀 Open your browser to: http://127.0.0.1:8000"
    echo "⏹️  Press Ctrl+C to stop the server"
    echo ""
    python manage.py runserver
else
    echo "❌ System check failed!"
    exit 1
fi
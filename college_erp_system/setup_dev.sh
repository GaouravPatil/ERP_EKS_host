#!/bin/bash

# College ERP Development Setup Script
# This script sets up the development environment

echo "🎓 College ERP Development Setup"
echo "================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>/dev/null || echo "Not found")
if [[ $python_version == *"Python 3."* ]]; then
    print_status "Python 3 found: $python_version"
else
    print_error "Python 3 is required but not found"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
if [ $? -eq 0 ]; then
    print_status "Virtual environment activated"
else
    print_error "Failed to activate virtual environment"
    exit 1
fi

# Install requirements
echo "Installing requirements..."
pip install --upgrade pip
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    print_status "Requirements installed successfully"
else
    print_error "Failed to install requirements"
    exit 1
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    print_status ".env file created"
    print_warning "Please edit .env file with your configuration"
else
    print_status ".env file already exists"
fi

# Run migrations
echo "Running database migrations..."
python manage.py migrate
if [ $? -eq 0 ]; then
    print_status "Database migrations completed"
else
    print_error "Database migrations failed"
    exit 1
fi

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput
if [ $? -eq 0 ]; then
    print_status "Static files collected"
else
    print_warning "Static files collection failed (this is okay for development)"
fi

# Ask if user wants to create sample data
echo ""
read -p "Do you want to create sample data for testing? (y/n): " create_sample
if [[ $create_sample =~ ^[Yy]$ ]]; then
    echo "Creating sample data..."
    python manage.py create_sample_data
    if [ $? -eq 0 ]; then
        print_status "Sample data created successfully"
        echo ""
        echo "🔐 Demo Login Credentials:"
        echo "   (Check the output above for generated usernames)"
        echo "   Password for all demo users: change_this_password_123"
        echo ""
        print_warning "Please change these passwords immediately after login!"
    else
        print_error "Failed to create sample data"
    fi
fi

echo ""
echo "🎉 Setup Complete!"
echo "==================="
echo ""
echo "To start the development server:"
echo "1. Make sure virtual environment is activated:"
echo "   source venv/bin/activate    # Linux/Mac"
echo "   venv\\Scripts\\activate        # Windows"
echo ""
echo "2. Start the server:"
echo "   python manage.py runserver"
echo ""
echo "3. Open your browser to:"
echo "   http://127.0.0.1:8000"
echo ""
echo "📝 Don't forget to:"
echo "   - Edit .env file with your institution details"
echo "   - Change demo passwords after first login"
echo "   - Configure email settings if needed"
echo ""
echo "📖 Read OPTIMIZATION_SUMMARY.md for detailed changes"
echo ""
print_status "Happy coding! 🚀"
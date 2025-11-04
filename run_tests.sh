#!/bin/bash

# DevMeter Test Runner
set -e

echo "🍅 DevMeter - Running Test Suite"
echo "================================="

# Check if we're in the right directory
if [ ! -f "requirements-dev.txt" ]; then
    echo "❌ Error: requirements-dev.txt not found. Are you in the project root?"
    exit 1
fi

# Install dependencies if needed
echo "📦 Installing dependencies..."
pip install -r requirements-dev.txt

# Run tests
echo "🧪 Running tests..."
pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

# Run linting
echo "🔍 Running linting..."
python -m flake8 src/ tests/ --max-line-length=100 --extend-ignore=E203,W503 || true

# Check if Docker is available and run container tests
if command -v docker &> /dev/null; then
    echo "🐳 Testing Docker build..."
    docker build -t devmeter-test .

    echo "🚀 Testing container startup..."
    docker run -d --name devmeter-test-container -p 8081:8080 devmeter-test
    sleep 10

    echo "🏥 Testing health endpoint..."
    if curl -f http://localhost:8081/health &> /dev/null; then
        echo "✅ Health check passed"
    else
        echo "❌ Health check failed"
        docker logs devmeter-test-container
        docker stop devmeter-test-container
        docker rm devmeter-test-container
        exit 1
    fi

    echo "🧹 Cleaning up test container..."
    docker stop devmeter-test-container
    docker rm devmeter-test-container
    docker rmi devmeter-test
fi

echo ""
echo "🎉 All tests completed successfully!"
echo "📊 Coverage report: htmlcov/index.html"
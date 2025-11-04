#!/bin/bash

# DevMeter Integration Test Runner
# Runs real HTTP tests against the running application

set -e

echo "🍅 DevMeter - Integration Test Suite"
echo "===================================="

# Check if we're in the right directory
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt not found. Are you in the project root?"
    exit 1
fi

# Check if Docker is available
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed or not in PATH"
    exit 1
fi

# Clean up any existing test containers
echo "🧹 Cleaning up existing test containers..."
docker stop devmeter-integration-test 2>/dev/null || true
docker rm devmeter-integration-test 2>/dev/null || true
docker rmi devmeter-test 2>/dev/null || true

# Install test dependencies
echo "📦 Installing test dependencies..."
pip install -r requirements-dev.txt

# Build the test image
echo "🏗️ Building DevMeter test image..."
docker build -t devmeter-test .

# Run the integration tests
echo "🧪 Running integration tests..."
python -m pytest tests/test_integration.py -v -s --tb=short

# Clean up
echo "🧹 Cleaning up test resources..."
docker stop devmeter-integration-test 2>/dev/null || true
docker rm devmeter-integration-test 2>/dev/null || true
docker rmi devmeter-test 2>/dev/null || true

echo ""
echo "🎉 Integration tests completed successfully!"
echo "✅ Real DevMeter application tested with live HTTP calls"
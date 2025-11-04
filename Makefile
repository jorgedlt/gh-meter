# DevMeter - GitHub Developer Rating System
.PHONY: help install test run build clean deploy

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements-dev.txt

install-prod: ## Install production dependencies
	pip install -r requirements.txt

test: ## Run test suite
	pytest tests/ -v --cov=src --cov-report=html

test-unit: ## Run unit tests only
	pytest tests/ -v -k "not integration"

lint: ## Run code linting
	flake8 src/ tests/ --max-line-length=100

format: ## Format code with black
	black src/ tests/

run: ## Run development server
	cd src && python app.py

run-docker: ## Run with Docker Compose
	docker-compose up --build

build: ## Build Docker image
	docker build -t devmeter .

clean: ## Clean up Docker containers and images
	docker-compose down -v
	docker system prune -f
	docker image rm devmeter 2>/dev/null || true

deploy-local: ## Deploy locally with Docker
	docker build -t devmeter .
	docker run -p 8080:8080 -e FLASK_DEBUG=true devmeter

health-check: ## Check if service is healthy
	curl -f http://localhost:8080/health || exit 1

smoke-test: ## Run basic smoke tests
	@echo "Running smoke tests..."
	@make health-check
	@echo "Testing main page..."
	@curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/ | grep -q "200" || (echo "Main page failed" && exit 1)
	@echo "Testing API endpoint..."
	@curl -s -X POST http://localhost:8080/analyze \
		-H "Content-Type: application/json" \
		-d '{"url":"https://github.com/octocat"}' \
		-o /dev/null -w "%{http_code}" | grep -q "200" || (echo "API test failed" && exit 1)
	@echo "✅ All smoke tests passed!"

setup: ## Initial project setup
	pre-commit install
	pip install -r requirements-dev.txt

update-deps: ## Update dependencies
	pip-compile requirements.in
	pip-compile requirements-dev.in

# Development helpers
logs: ## Show Docker Compose logs
	docker-compose logs -f

shell: ## Open shell in running container
	docker-compose exec devmeter bash

db-shell: ## Open database shell (if applicable)
	docker-compose exec db psql -U postgres -d devmeter
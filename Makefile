.PHONY: help install run dev test clean lint format

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make run        - Run the application"
	@echo "  make dev        - Run in development mode with auto-reload"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linting"
	@echo "  make format     - Format code"
	@echo "  make clean      - Clean cache files"

install:
	pip install -r requirements.txt

run:
	uvicorn src.main:app --host 0.0.0.0 --port 8000

dev:
	uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

test:
	pytest -v

test-cov:
	pytest --cov=src --cov-report=html --cov-report=term

lint:
	flake8 src/ --max-line-length=120

format:
	black src/ tests/
	isort src/ tests/

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

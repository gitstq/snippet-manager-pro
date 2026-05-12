.PHONY: help install install-dev test lint format clean build upload

help:
	@echo "CodeSnippet Pro - Available Commands:"
	@echo "  make install      - Install package"
	@echo "  make install-dev  - Install with development dependencies"
	@echo "  make test         - Run tests"
	@echo "  make lint         - Run linters"
	@echo "  make format       - Format code with black"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make build        - Build package"
	@echo "  make upload       - Upload to PyPI"

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest tests/ -v --cov=codesnippet_pro --cov-report=term-missing

lint:
	flake8 src/codesnippet_pro tests
	mypy src/codesnippet_pro

format:
	black src/codesnippet_pro tests

clean:
	rm -rf build/ dist/ *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete

build: clean
	python -m build

upload: build
	python -m twine upload dist/*

dev:
	python -m codesnippet_pro.cli interactive

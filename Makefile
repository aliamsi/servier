# Variables
PYTHON := python3
PIP := pip
PYTEST := pytest
COVERAGE := coverage
PYLINT := pylint
BLACK := black
ISORT := isort
PYTHON_FILES := src/ tests/ config/

# Virtual environment
VENV := .venv
VENV_BIN := $(VENV)/bin
VENV_ACTIVATE := . $(VENV_BIN)/activate

# Help message for available commands
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install         - Install package and dependencies"
	@echo "  make install-dev     - Install development dependencies"
	@echo "  make test           - Run tests"
	@echo "  make coverage       - Run tests with coverage report"
	@echo "  make lint           - Run linting checks"
	@echo "  make format         - Format code with black and isort"
	@echo "  make clean          - Clean up build and cache files"
	@echo "  make venv           - Create virtual environment"
	@echo "  make requirements   - Generate requirements.txt files"
	@echo "  make check-all      - Run all checks (lint, format, test)"

# Virtual environment setup
.PHONY: venv
venv:
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip setuptools wheel

# Installation
.PHONY: install
install: venv
	$(VENV_BIN)/pip install -e .

.PHONY: install-dev
install-dev: install
	$(VENV_BIN)/pip install -e ".[test]"
	$(VENV_BIN)/pip install pylint black isort sphinx

# Testing
.PHONY: test
test:
	$(VENV_BIN)/$(PYTEST) tests/ -v

.PHONY: coverage
coverage:
	$(VENV_BIN)/$(PYTEST) --cov=src --cov-report=term-missing --cov-report=html tests/

# Linting and formatting
.PHONY: lint
lint:
	$(VENV_BIN)/$(PYLINT) $(PYTHON_FILES)

.PHONY: format
format:
	$(VENV_BIN)/$(BLACK) $(PYTHON_FILES)
	$(VENV_BIN)/$(ISORT) $(PYTHON_FILES)

.PHONY: check-format
check-format:
	$(VENV_BIN)/$(BLACK) --check $(PYTHON_FILES)
	$(VENV_BIN)/$(ISORT) --check-only $(PYTHON_FILES)

# Combined checks
.PHONY: check-all
check-all: lint check-format coverage

# Requirements
.PHONY: requirements
requirements:
	$(VENV_BIN)/pip freeze > requirements.txt
	$(VENV_BIN)/pip freeze | grep -v -f requirements.txt > requirements-dev.txt

# Pipeline execution
.PHONY: run
run:
	$(VENV_BIN)/python pipeline.py

# Development workflow shortcuts
.PHONY: dev-setup
dev-setup: venv install-dev init

.PHONY: dev-update
dev-update: clean install-dev format check-all
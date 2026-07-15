# Local development Makefile for StatsApp

PYTHON ?= python3
VENV ?= venv
PYTHON_VENV := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
ENV_FILE := .env
FRONTEND_DIR := frontend

.PHONY: help setup env migrate bootstrap run backend frontend-install frontend-dev full-setup clean

help:
	@echo "Usage: make <target>"
	@echo "Available targets:"
	@echo "  setup           Create virtualenv, install Python dependencies, and install frontend packages"
	@echo "  env             Copy .env.example to .env if missing"
	@echo "  migrate         Run Django migrations"
	@echo "  bootstrap       Seed local development data"
	@echo "  backend         Run the Django development server"
	@echo "  frontend-install  Install frontend npm dependencies"
	@echo "  frontend-dev    Start the frontend Vite dev server"
	@echo "  full-setup      Run setup, env, migrate, and bootstrap"
	@echo "  clean           Remove virtualenv and temp files"

setup: $(VENV) frontend-install
	@echo "Python virtualenv created and dependencies installed."

$(VENV):
	@echo "Creating Python virtual environment..."
	$(PYTHON) -m venv $(VENV)
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt

env:
	@if [ ! -f $(ENV_FILE) ]; then \
		cp .env.example $(ENV_FILE); \
		echo "Created $(ENV_FILE) from .env.example"; \
	else \
		echo "$(ENV_FILE) already exists"; \
	fi

migrate:
	@echo "Running Django migrations..."
	@$(PYTHON_VENV) manage.py makemigrations
	@$(PYTHON_VENV) manage.py migrate

bootstrap:
	@echo "Seeding local development data..."
	@$(PYTHON_VENV) bootstrap_dev.py

run: backend

backend:
	@echo "Starting Django development server..."
	@$(PYTHON_VENV) manage.py runserver 0.0.0.0:8000

frontend-install:
	@echo "Installing frontend dependencies..."
	@cd $(FRONTEND_DIR) && npm install

frontend-dev:
	@echo "Starting frontend Vite dev server..."
	@cd $(FRONTEND_DIR) && npm run dev

full-setup: setup env migrate bootstrap
	@echo "Local development environment is ready."

clean:
	@echo "Removing virtual environment..."
	@rm -rf $(VENV)
	@echo "Cleaned up $(VENV)"

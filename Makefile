# Makefile for Langflow Docker setup

.PHONY: setup start stop restart logs clean status help

help:
	@echo "Langflow Docker Setup - Available commands:"
	@echo "  make setup    - Create necessary directories and copy .env.example to .env"
	@echo "  make start    - Start Langflow containers"
	@echo "  make stop     - Stop Langflow containers"
	@echo "  make restart  - Restart Langflow containers"
	@echo "  make logs     - View Langflow container logs"
	@echo "  make clean    - Stop containers and remove volumes"
	@echo "  make status   - Check status of containers"

setup:
	@echo "Setting up Langflow..."
	mkdir -p custom_components data/langflow data/postgres
	cp -n .env.example .env 2>/dev/null || true
	@echo "Setup complete. Edit .env file if needed, then run 'make start'"

start:
	@echo "Starting Langflow containers..."
	@echo "Initializing volumes with proper permissions..."
	docker compose up init-volumes --build
	@echo "Starting main services..."
	docker compose up -d
	@PORT=$$(grep LANGFLOW_PORT .env | cut -d= -f2 | cut -d' ' -f1 || echo 7860); \
	echo "Langflow is running at http://localhost:$$PORT"

stop:
	@echo "Stopping Langflow containers..."
	docker compose down

restart:
	@echo "Restarting Langflow containers..."
	docker compose restart
	@PORT=$$(grep LANGFLOW_PORT .env | cut -d= -f2 | cut -d' ' -f1 || echo 7860); \
	echo "Langflow is running at http://localhost:$$PORT"

logs:
	@echo "Showing Langflow logs (Ctrl+C to exit)..."
	docker compose logs -f

clean:
	@echo "Cleaning up Langflow containers and volumes..."
	docker compose down
	@echo "Cleanup complete"

clean-all:
	@echo "Cleaning up Langflow containers and removing all data..."
	docker compose down
	rm -rf data/langflow/* data/postgres/*
	@echo "Complete cleanup done. All data has been removed."

status:
	@echo "Checking Langflow container status..."
	docker compose ps 
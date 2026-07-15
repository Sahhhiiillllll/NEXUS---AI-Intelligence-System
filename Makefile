# N.A.X.U.S — Makefile
# ======================
# Common development tasks

.PHONY: help build run dev test lint clean docker-compose-up docker-compose-down logs

# Default target
help:
	@echo "N.A.X.U.S Development Tasks:"
	@echo "  make build           - Build Docker image"
	@echo "  make run             - Run the application (Docker)"
	@echo "  make dev             - Run in development mode (localhost)"
	@echo "  make test            - Run test suite"
	@echo "  make lint            - Run linting (if configured)"
	@echo "  make docker-compose-up - Start services with docker-compose"
	@echo "  make docker-compose-down - Stop docker-compose services"
	@echo "  make logs            - View container logs"
	@echo "  make clean           - Remove temporary files"

# Docker targets
build:
	docker build -t nexus .

run:
	docker run --rm -it \
		-p 8765:8765 \
		-p 8865:8865 \
		-v $(PWD)/logs:/app/logs:rw \
		-v $(PWD)/.env:/app/.env:ro \
		-e NEXUS_HOST=0.0.0.0 \
		-e NEXUS_PORT=8765 \
		nexus

dev:
	python main.py

test:
	pytest tests.py -v

lint:
	# Add linting configuration if needed (flake8, pylint, etc.)
	@echo "Linting not configured - add flake8/pylint config if desired"

docker-compose-up:
	docker-compose up -d

docker-compose-down:
	docker-compose down

logs:
	docker-compose logs -f

clean:
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf *.pyc */*.pyc */*/*.pyc
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
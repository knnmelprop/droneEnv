SHELL := /usr/bin/bash
.DEFAULT_GOAL := help

help:
	@echo "Common targets:"
	@echo "  make build         - Build local Docker image"
	@echo "  make up            - Start Jupyter container"
	@echo "  make down          - Stop and remove container"
	@echo "  make bash          - Open bash in running container"
	@echo "  make dev-install   - Developer install SUAVE (setup.py develop) inside container"

build:
	docker compose build

up:
	docker compose up -d
	@sleep 1; docker compose logs -f suave | sed -n '1,80p'

logs:
	docker compose logs -f suave | cat

down:
	docker compose down -v

bash:
	docker compose exec suave bash

# Install SUAVE in editable mode inside container
# Assumes repo mounted at /workspace
dev-install:
	docker compose exec suave bash -lc 'cd trunk && python setup.py develop'
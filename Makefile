SERVICE_NAME = bot

.PHONY: up bash migrate

up:
	docker compose up -d

bash:
	docker exec -it $(SERVICE_NAME) bash

migrate:
	docker exec -it $(SERVICE_NAME) alembic upgrade head

all: up migrate

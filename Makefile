# Работа через Docker

build:
	docker compose pull --ignore-buildable
	docker compose build

run:
	docker compose up -d

stop:
	docker compose down -v

pytest:
	docker compose run --rm django pytest

makemigrations:
	docker compose run --rm django ./manage.py makemigrations

migrate:
	docker compose run --rm django ./manage.py migrate

first_start:
	make build migrate

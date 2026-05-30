.PHONY: help build up down logs shell migrate static test clean restart

help:
	@echo "ATM Bank Docker Commands"
	@echo "========================"
	@echo "make build          - Build Docker images"
	@echo "make up             - Start all containers"
	@echo "make down           - Stop and remove containers"
	@echo "make logs           - View container logs"
	@echo "make shell          - Access Django shell"
	@echo "make bash           - Access container bash"
	@echo "make db-shell       - Access PostgreSQL shell"
	@echo "make migrate        - Run database migrations"
	@echo "make static         - Collect static files"
	@echo "make superuser      - Create superuser"
	@echo "make test           - Run tests"
	@echo "make clean          - Remove containers and volumes"
	@echo "make restart        - Restart containers"
	@echo "make logs-web       - View web container logs"
	@echo "make logs-db        - View database logs"
	@echo "make logs-nginx     - View nginx logs"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✓ Containers started!"
	@echo "  Web: http://localhost"
	@echo "  Direct: http://localhost:8000"

down:
	docker-compose down
	@echo "✓ Containers stopped!"

logs:
	docker-compose logs -f

logs-web:
	docker-compose logs -f web

logs-db:
	docker-compose logs -f db

logs-nginx:
	docker-compose logs -f nginx

shell:
	docker-compose exec web python manage.py shell

bash:
	docker-compose exec web bash

db-shell:
	docker-compose exec db psql -U atm_user -d atm_db

migrate:
	docker-compose exec web python manage.py migrate
	@echo "✓ Migrations completed!"

static:
	docker-compose exec web python manage.py collectstatic --noinput --clear
	@echo "✓ Static files collected!"

superuser:
	docker-compose exec web python manage.py createsuperuser

test:
	docker-compose exec web python manage.py test

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✓ Cleaned up!"

restart:
	docker-compose restart
	@echo "✓ Containers restarted!"

ps:
	docker-compose ps

check:
	docker-compose exec web python manage.py check

version:
	docker-compose --version
	docker --version

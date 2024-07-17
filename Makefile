build:
	docker-compose build
up:
	docker-compose up -d
down:
	docker-compose down
stop:
	docker-compose stop
restart:
	docker-compose restart
migrations:
	@echo 'Migration Name: '; \
	read NAME; \
	alembic -c api/alembic.ini revision --autogenerate -m "$$NAME"
migrate:
	alembic -c api/alembic.ini upgrade head

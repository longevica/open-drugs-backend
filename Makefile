include .env
export $(shell sed 's/=.*//' .env)

migrate_up:
	yoyo apply --database ${DB_CONN} -b ./api/db/migrations

migrate_down:
	yoyo rollback --database ${DB_CONN} ./api/db/migrations

build:
	export DOCKER_DEFAULT_PLATFORM=linux/amd64
	./listcontrols-backend.sh build

run:
	./listcontrols-backend.sh run api

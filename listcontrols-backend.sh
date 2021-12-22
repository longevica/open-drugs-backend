#!/bin/bash
uid=$(id -u)
gid=$(id -g)
USAGE="usage: $0 <docker-compose args> [scripts]\nexamples:\n ./$0 build\n ./$0 run api\n ./$0 run scripts"

COMPOSE_ARGS=$*

[ "$COMPOSE_ARGS" = "" ] && echo $USAGE && exit

if [ "$COMPOSE_ARGS" = "up " ]
then
	COMPOSE_ARGS="up -d"
fi

mkdir -p ../listcontrols-logs
mkdir -p ../listcontrols-postgres

if [ ! -e .env ]
then
    cp .env.sample .env
    echo ".env copied"
fi

[ -f VERSION ] || touch VERSION

LISTCONTROLS_UID=$uid:$gid
export LISTCONTROLS_UID

docker network create postgres_net || true
docker-compose $COMPOSE_ARGS

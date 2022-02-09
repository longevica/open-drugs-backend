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

mkdir -p ../mice_lifespan-logs
mkdir -p ../mice_lifespan-postgres

if [ ! -e .env ]
then
    cp .env.sample .env
    echo ".env copied"
fi

[ -f VERSION ] || touch VERSION

MICE_LIFESPAN_UID=$uid:$gid
export MICE_LIFESPAN_UID

docker network create postgres_mice_lifespan_net || true
docker-compose $COMPOSE_ARGS

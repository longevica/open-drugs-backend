# mice_lifespan-backend
 Lifespan Studies Control Groups Backend

## Architecture

- **api** - API application root
    - *main.py* - entry point
    - **endpoints** - api endpoints
    - **db** - domain access object (DAO) logic for DB
    - **entities** - domain entities

## Development

### Build local development image

```
make build
```

### Run API app in development mode

```
make run
```

### DB migrations
- #### migrations up:
```
make migrate_up
```
- #### migrations down:
```
make migrate_down
```
